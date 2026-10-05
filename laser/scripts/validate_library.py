#!/usr/bin/env python3
"""Validate generated Technology Commons laser assets and metadata.

SPDX-License-Identifier: CC-BY-SA-4.0
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
GENERATED = ROOT / "generated"
CATALOG = GENERATED / "catalog.json"
SVG_NS = "{http://www.w3.org/2000/svg}"
REQUIRED = {
    "id", "title", "description", "category", "subcategory", "shop", "tool_family",
    "tags", "skill_level", "dimensions", "units", "material", "fit_type",
    "kerf_assumptions", "generator", "parameters", "operations", "files", "editors",
    "license", "attribution", "source_reference", "sensitivity", "trademark_status",
    "review_status", "notes",
}
VALID_REVIEW = {"unverified", "dimension-tested", "fit-tested", "shop-tested"}
VALID_OPERATIONS = {"CUT", "SCORE", "ENGRAVE"}
NUMBER_RE = re.compile(r"(?<![A-Za-z])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?")


class ValidationError(RuntimeError):
    pass


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def local_name(tag: str) -> str:
    return tag.split("}")[-1]


def parse_mm(value: str | None) -> float | None:
    if not value or not value.endswith("mm"):
        return None
    try:
        return float(value[:-2])
    except ValueError:
        return None


def element_signature(element: ET.Element) -> tuple[str, tuple[tuple[str, str], ...]]:
    ignored = {"data-operation", "data-closed", "vector-effect", "stroke", "stroke-width", "fill"}
    return local_name(element.tag), tuple(sorted((k, v) for k, v in element.attrib.items() if k not in ignored))


def validate_svg(path: Path, record: dict[str, Any], errors: list[str]) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        fail(errors, f"{path}: invalid SVG/XML: {exc}")
        return
    if root.tag != SVG_NS + "svg":
        fail(errors, f"{path}: root element is not SVG")
        return
    width = parse_mm(root.get("width"))
    height = parse_mm(root.get("height"))
    if width is None or height is None:
        fail(errors, f"{path}: fabrication width/height must use mm")
    expected = record["dimensions"]
    if width is not None and not math.isclose(width, float(expected["width"]), abs_tol=0.0001):
        fail(errors, f"{path}: width {width} does not match manifest {expected['width']}")
    if height is not None and not math.isclose(height, float(expected["height"]), abs_tol=0.0001):
        fail(errors, f"{path}: height {height} does not match manifest {expected['height']}")
    view_box = root.get("viewBox", "").split()
    if len(view_box) != 4:
        fail(errors, f"{path}: missing or invalid viewBox")
    else:
        try:
            values = [float(value) for value in view_box]
            if values[:2] != [0.0, 0.0] or not math.isclose(values[2], float(expected["width"]), abs_tol=0.0001) or not math.isclose(values[3], float(expected["height"]), abs_tol=0.0001):
                fail(errors, f"{path}: viewBox does not match intended dimensions")
        except ValueError:
            fail(errors, f"{path}: non-numeric viewBox")

    raw = path.read_text(encoding="utf-8")
    lowered = raw.lower()
    if "<image" in lowered or "data:image" in lowered:
        fail(errors, f"{path}: embedded raster content is forbidden")
    if "@font-face" in lowered or "url(" in lowered:
        fail(errors, f"{path}: external fonts/resources are forbidden")
    if "<use" in lowered or "xlink:href" in lowered or " href=" in lowered:
        fail(errors, f"{path}: external/reused geometry is forbidden in fabrication SVGs")
    if " transform=" in lowered:
        fail(errors, f"{path}: transforms are forbidden in canonical generated geometry")
    for token in NUMBER_RE.findall(raw):
        if not math.isfinite(float(token)):
            fail(errors, f"{path}: non-finite coordinate")
            break

    metadata_nodes = root.findall(SVG_NS + "metadata")
    if len(metadata_nodes) != 1:
        fail(errors, f"{path}: exactly one metadata element is required")
    else:
        try:
            embedded = json.loads(metadata_nodes[0].text or "")
            if embedded.get("id") != record["id"]:
                fail(errors, f"{path}: embedded metadata ID mismatch")
        except json.JSONDecodeError as exc:
            fail(errors, f"{path}: embedded metadata is not JSON: {exc}")

    drawable = {"rect", "circle", "ellipse", "line", "polygon", "polyline", "path", "text"}
    signatures: Counter[tuple[str, tuple[tuple[str, str], ...]]] = Counter()
    operations: set[str] = set()
    for element in root.iter():
        name = local_name(element.tag)
        if name not in drawable:
            continue
        operation = element.get("data-operation")
        if operation not in VALID_OPERATIONS:
            fail(errors, f"{path}: {name} missing valid data-operation")
        else:
            operations.add(operation)
        if name != "text":
            signatures[element_signature(element)] += 1
        if name == "line":
            if element.get("x1") == element.get("x2") and element.get("y1") == element.get("y2"):
                fail(errors, f"{path}: zero-length line")
        if name == "path":
            d = element.get("d", "").strip()
            if not d or len(NUMBER_RE.findall(d)) < 2:
                fail(errors, f"{path}: empty or zero-length path")
            if element.get("data-closed") == "true" and "z" not in d.lower():
                fail(errors, f"{path}: path marked closed does not end with Z")
        if name in {"rect", "circle", "ellipse", "polygon"} and operation == "CUT" and element.get("data-closed") != "true":
            fail(errors, f"{path}: closed cut geometry is not marked closed")
    duplicate = [signature for signature, count in signatures.items() if count > 1]
    if duplicate:
        fail(errors, f"{path}: duplicate geometry detected: {duplicate[0]}")
    if operations != set(record["operations"]):
        fail(errors, f"{path}: operations {sorted(operations)} do not match manifest {record['operations']}")


def validate_manifest(document: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    assets = document.get("assets")
    if not isinstance(assets, list) or not assets:
        return ["catalog.json: assets must be a non-empty list"]
    if document.get("count") != len(assets):
        fail(errors, "catalog.json: count does not match asset list")
    ids = [record.get("id") for record in assets]
    duplicates = [value for value, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(errors, f"catalog.json: duplicate IDs: {duplicates}")
    if len(assets) < 150:
        fail(errors, f"catalog.json: meaningful first catalogue requires at least 150 assets; found {len(assets)}")
    for index, record in enumerate(assets):
        label = record.get("id", f"record {index}")
        missing = sorted(REQUIRED - set(record))
        if missing:
            fail(errors, f"{label}: missing metadata fields {missing}")
            continue
        if record["units"] != "mm":
            fail(errors, f"{label}: units must be mm")
        if record["review_status"] not in VALID_REVIEW:
            fail(errors, f"{label}: invalid review status")
        if not record["license"]:
            fail(errors, f"{label}: missing license")
        if not set(record["operations"]).issubset(VALID_OPERATIONS):
            fail(errors, f"{label}: invalid operation")
        for kind in ("svg", "preview"):
            rel = record["files"].get(kind)
            if not rel or not (ROOT / rel).is_file():
                fail(errors, f"{label}: missing {kind} file {rel}")
        svg_path = ROOT / record["files"]["svg"]
        if svg_path.is_file():
            validate_svg(svg_path, record, errors)
    category_counts = Counter(record["category"] for record in assets)
    if dict(sorted(category_counts.items())) != document.get("category_counts"):
        fail(errors, "catalog.json: category_counts mismatch")
    bundle = GENERATED / "downloads" / "technology-commons-laser-library.zip"
    if not bundle.is_file() or bundle.stat().st_size == 0:
        fail(errors, "download bundle is missing or empty")
    if not (GENERATED / "SHA256SUMS").is_file():
        fail(errors, "SHA256SUMS is missing")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit a JSON validation report")
    args = parser.parse_args()
    if not CATALOG.is_file():
        print("catalog.json is missing; run generate_library.py", file=sys.stderr)
        return 1
    document = json.loads(CATALOG.read_text(encoding="utf-8"))
    errors = validate_manifest(document)
    report = {"ok": not errors, "asset_count": document.get("count", 0), "errors": errors}
    if args.json:
        print(json.dumps(report, indent=2))
    elif errors:
        print(f"Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"Validated {report['asset_count']} laser fabrication assets")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
