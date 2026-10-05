#!/usr/bin/env python3
"""Generate the Technology Commons laser fabrication catalogue.

SPDX-License-Identifier: CC-BY-SA-4.0
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import math
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml

from generate_classroom_kit import main as generate_classroom_kit

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "library.yml"
GENERATED = ROOT / "generated"
SVG_ROOT = GENERATED / "svg"
PREVIEW_ROOT = GENERATED / "previews"
GENERATOR_NAME = "technology-commons-laser-generator"

STYLE = {
    "CUT": 'fill="none" stroke="#ff0000" stroke-width="0.1" vector-effect="non-scaling-stroke"',
    "SCORE": 'fill="none" stroke="#0000ff" stroke-width="0.1" vector-effect="non-scaling-stroke"',
    "ENGRAVE": 'fill="none" stroke="#000000" stroke-width="0.18" vector-effect="non-scaling-stroke"',
}


def n(value: float) -> str:
    """Stable compact decimal formatting."""
    return f"{value:.4f}".rstrip("0").rstrip(".") or "0"


def attrs(operation: str, closed: bool | None = None) -> str:
    result = f'{STYLE[operation]} data-operation="{operation}"'
    if closed is not None:
        result += f' data-closed="{str(closed).lower()}"'
    return result


def rect(x: float, y: float, width: float, height: float, operation: str = "CUT", rx: float = 0) -> str:
    rounded = f' rx="{n(rx)}" ry="{n(rx)}"' if rx else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(width)}" height="{n(height)}"{rounded} {attrs(operation, True)}/>'


def circle(cx: float, cy: float, radius: float, operation: str = "CUT") -> str:
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(radius)}" {attrs(operation, True)}/>'


def ellipse(cx: float, cy: float, rx: float, ry: float, operation: str = "CUT") -> str:
    return f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" {attrs(operation, True)}/>'


def line(x1: float, y1: float, x2: float, y2: float, operation: str = "SCORE") -> str:
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" {attrs(operation, False)}/>'


def polygon(points: Iterable[tuple[float, float]], operation: str = "CUT") -> str:
    value = " ".join(f"{n(x)},{n(y)}" for x, y in points)
    return f'<polygon points="{value}" {attrs(operation, True)}/>'


def path(d: str, operation: str = "CUT", closed: bool = True) -> str:
    return f'<path d="{d}" {attrs(operation, closed)}/>'


def label(x: float, y: float, value: str, size: float = 3.2, anchor: str = "start") -> str:
    return (
        f'<text x="{n(x)}" y="{n(y)}" font-family="sans-serif" font-size="{n(size)}" '
        f'text-anchor="{anchor}" fill="#000000" stroke="none" data-operation="ENGRAVE">'
        f'{html.escape(value)}</text>'
    )


def star_points(cx: float, cy: float, outer: float, inner: float, count: int = 5) -> list[tuple[float, float]]:
    points = []
    for i in range(count * 2):
        angle = -math.pi / 2 + i * math.pi / count
        radius = outer if i % 2 == 0 else inner
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return points


def regular_polygon(cx: float, cy: float, radius: float, sides: int) -> list[tuple[float, float]]:
    return [
        (cx + radius * math.cos(-math.pi / 2 + i * 2 * math.pi / sides),
         cy + radius * math.sin(-math.pi / 2 + i * 2 * math.pi / sides))
        for i in range(sides)
    ]


@dataclass
class Asset:
    id: str
    title: str
    description: str
    category: str
    subcategory: str
    width: float
    height: float
    geometry: list[str]
    shop: str = "general"
    tool_family: str = "none"
    tags: list[str] = field(default_factory=list)
    technology_areas: list[str] = field(default_factory=list)
    skill_level: str = "introductory"
    fit_type: str = "none"
    parameters: dict[str, Any] = field(default_factory=dict)
    operations: list[str] = field(default_factory=lambda: ["CUT"])
    editors: list[str] = field(default_factory=lambda: ["Inkscape", "Vectorpea"])
    sensitivity: str = "none"
    trademark_status: str = "original-generic"
    review_status: str = "unverified"
    notes: str = "Verify dimensions and local machine operation mapping before fabrication."
    source_reference: str = "Original procedural geometry; no traced or copied commercial artwork."
    tests: dict[str, float] = field(default_factory=dict)


TECHNOLOGY_AREAS = {
    "exploring-technologies", "technological-design", "manufacturing", "construction",
    "transportation", "computer-technology", "communications-technology", "green-industries",
    "hairstyling-aesthetics", "hospitality-tourism", "health-care",
}


def technology_areas_for(asset: Asset) -> list[str]:
    """Return selective curriculum contexts supported by an asset's actual form and use."""
    areas = {"exploring-technologies", "technological-design"}
    identifier = asset.id

    if asset.category in {"calibration", "french-cleat"}:
        areas.add("manufacturing")
    if asset.category == "french-cleat":
        areas.add("construction")

    shop_areas = {
        "machine": {"manufacturing"},
        "auto": {"transportation", "manufacturing"},
        "wood": {"construction"},
        "electronics": {"computer-technology"},
    }
    areas.update(shop_areas.get(asset.shop, set()))

    if asset.category == "jigs-gauges":
        if any(term in identifier for term in ("pcb", "cable-wire")):
            areas.add("computer-technology")
        if any(term in identifier for term in ("shelf", "sanding", "drill-spacing", "screw-length")):
            areas.add("construction")
        if any(term in identifier for term in ("fastener", "wrench", "bolt-circle", "drill-size", "setup-block", "slot-width")):
            areas.add("manufacturing")
        if any(term in identifier for term in ("fastener", "wrench", "screw-length")):
            areas.add("transportation")

    if asset.category == "tool-holders":
        if any(term in identifier for term in ("cable", "test-lead", "precision-driver", "solder")):
            areas.add("communications-technology")
        if any(term in identifier for term in ("marker", "brush", "tweezer")):
            areas.add("hairstyling-aesthetics")

    if asset.category == "core-geometry":
        if asset.subcategory in {"label-plates", "frames"}:
            areas.add("communications-technology")
        if asset.subcategory == "label-plates":
            areas.update({"hospitality-tourism", "health-care"})
        if asset.subcategory == "mounting-patterns":
            areas.add("computer-technology")
        if asset.subcategory in {"brackets", "bolt-circles", "gussets", "hooks", "keyholes", "spacers"}:
            areas.update({"manufacturing", "construction"})

    if asset.category == "project-components":
        if any(term in identifier for term in ("sign", "plaque", "easel", "tag", "bookmark")):
            areas.add("communications-technology")
        if any(term in identifier for term in ("coaster", "sign", "easel")):
            areas.add("hospitality-tourism")
        if any(term in identifier for term in ("tag", "sign", "divider")):
            areas.add("hairstyling-aesthetics")
        if any(term in identifier for term in ("sign", "divider")):
            areas.add("health-care")
        if any(term in identifier for term in ("box", "divider", "joint", "leg", "foot")):
            areas.update({"manufacturing", "construction"})

    if asset.category == "themed-starters":
        areas.add("communications-technology")
        if asset.subcategory in {"nature", "animals"}:
            areas.add("green-industries")
        if asset.subcategory == "architecture" or "hard-hat" in identifier:
            areas.add("construction")
        if asset.subcategory == "transportation":
            areas.add("transportation")
        if asset.subcategory in {"technology", "science", "space"}:
            areas.add("computer-technology")
        if any(term in identifier for term in ("ppe", "safety-glasses", "caution", "exit")):
            areas.add("health-care")

    return sorted(areas)


class Catalogue:
    def __init__(self, config: dict[str, Any]):
        self.cfg = config["library"]
        self.assets: list[Asset] = []

    def add(self, asset: Asset) -> None:
        if not asset.tags:
            asset.tags = [asset.category, asset.subcategory]
        if not asset.technology_areas:
            asset.technology_areas = technology_areas_for(asset)
        self.assets.append(asset)

    def metadata(self, asset: Asset) -> dict[str, Any]:
        material = self.cfg["default_material"]
        fabrication = self.cfg["fabrication"]
        veccy_terms = (
            "disc-", "ring-", "rectangle-", "slot-", "hole-grid", "mount-",
            "cal-slot-fit", "cleat-module-face", "holder-", "frame-", "sign-blank",
            "easel", "cross-stand", "tab-slot", "shadow-board",
        )
        editors = list(asset.editors)
        if any(term in asset.id for term in veccy_terms) and "Veccy" not in editors:
            editors.insert(1, "Veccy")
        rel_svg = f"generated/svg/{asset.category}/{asset.id}.svg"
        rel_preview = f"generated/previews/{asset.category}/{asset.id}.svg"
        return {
            "id": asset.id,
            "title": asset.title,
            "description": asset.description,
            "category": asset.category,
            "subcategory": asset.subcategory,
            "shop": asset.shop,
            "tool_family": asset.tool_family,
            "tags": sorted(set(asset.tags)),
            "technology_areas": sorted(set(asset.technology_areas)),
            "skill_level": asset.skill_level,
            "dimensions": {"width": round(asset.width, 4), "height": round(asset.height, 4)},
            "units": "mm",
            "material": {
                "name": material["name"],
                "nominal": material["nominal"],
                "measured_thickness_mm": material["measured_thickness_mm"],
                "warning": material["warning"],
            },
            "fit_type": asset.fit_type,
            "kerf_assumptions": {
                "kerf_mm": fabrication["kerf_mm"],
                "clearance_mm": fabrication["clearance_mm"],
                "warning": "Starting values only; select from a physical calibration cut.",
            },
            "generator": {"name": GENERATOR_NAME, "version": self.cfg["generator_version"]},
            "parameters": asset.parameters,
            "operations": asset.operations,
            "files": {"svg": rel_svg, "preview": rel_preview},
            "editors": editors,
            "license": self.cfg["license"],
            "attribution": self.cfg["attribution"],
            "source_reference": asset.source_reference,
            "sensitivity": asset.sensitivity,
            "trademark_status": asset.trademark_status,
            "review_status": asset.review_status,
            "notes": asset.notes,
            "dimensional_tests": asset.tests,
        }


def svg_document(asset: Asset, metadata: dict[str, Any], preview: bool = False) -> str:
    if preview:
        width_attr = "640"
        height_attr = n(640 * asset.height / asset.width)
        background = f'<rect x="0" y="0" width="{n(asset.width)}" height="{n(asset.height)}" fill="#fffdf8"/>'
    else:
        width_attr = f"{n(asset.width)}mm"
        height_attr = f"{n(asset.height)}mm"
        background = ""
    # Technology-area discovery belongs in the catalogue. Keeping it out of the
    # embedded fabrication metadata avoids rewriting otherwise identical SVGs.
    embedded_metadata = {key: value for key, value in metadata.items() if key != "technology_areas"}
    meta_text = html.escape(json.dumps(embedded_metadata, sort_keys=True, separators=(",", ":")))
    groups = []
    for operation in ("CUT", "SCORE", "ENGRAVE"):
        items = [item for item in asset.geometry if f'data-operation="{operation}"' in item]
        if items:
            groups.append(f'<g id="{operation.lower()}" aria-label="{operation}">\n' + "\n".join(items) + "\n</g>")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width_attr}" height="{height_attr}" '
        f'viewBox="0 0 {n(asset.width)} {n(asset.height)}">\n'
        f'<title>{html.escape(asset.title)}</title>\n<desc>{html.escape(asset.description)}</desc>\n'
        f'<metadata id="technology-commons-metadata">{meta_text}</metadata>\n{background}\n'
        + "\n".join(groups)
        + "\n</svg>\n"
    )


def plate_geometry(width: float, height: float, rounded: float = 0) -> list[str]:
    return [rect(0, 0, width, height, rx=rounded)]


def add_calibration(c: Catalogue) -> None:
    thickness = float(c.cfg["default_material"]["measured_thickness_mm"])
    offsets = [float(v) for v in c.cfg["fabrication"]["fit_offsets_mm"]]
    # Dimension sheet: independent 50 mm circle and 100 x 100 square, with diagonal.
    geometry = [rect(10, 10, 100, 100), circle(160, 60, 25), line(10, 10, 110, 110),
                label(60, 118, "100.00 mm square", anchor="middle"),
                label(160, 94, "50.00 mm circle", anchor="middle"),
                label(110, 140, "MEASURE X, Y AND DIAGONAL", anchor="middle")]
    c.add(Asset("tc-cal-dimension-verification", "Dimension verification sheet",
        "A 100 mm square, diagonal and 50 mm circle for checking exported physical scale.",
        "calibration", "dimensions", 220, 150, geometry,
        tags=["calibration", "dimension", "circle", "square", "ruler"], operations=["CUT", "SCORE", "ENGRAVE"],
        tests={"square_width_mm": 100, "square_height_mm": 100, "circle_diameter_mm": 50}))

    geometry = [rect(5, 5, 200, 55), label(105, 13, "KERF TEST — measure removed comb width", anchor="middle")]
    for i in range(12):
        x = 20 + i * 14
        geometry.append(line(x, 22, x, 52, "CUT"))
    geometry += [line(15, 22, 190, 22, "SCORE"), label(105, 58, "12 cut lines · kerf = (reference − result) / 12", 2.8, "middle")]
    c.add(Asset("tc-cal-kerf-test", "Kerf test comb", "Twelve parallel cut lines for measuring average machine/material kerf.",
        "calibration", "kerf", 210, 65, geometry, fit_type="measurement",
        tags=["calibration", "kerf", "comb"], operations=["CUT", "SCORE", "ENGRAVE"], parameters={"cut_count": 12}))

    def gauge(asset_id: str, title: str, subtype: str, feature: str) -> None:
        geometry = [rect(5, 5, 200, 65), label(105, 13, title.upper(), anchor="middle")]
        for i, offset in enumerate(offsets):
            size = thickness + offset
            x = 15 + i * 27
            if feature == "slot":
                geometry.append(path(f"M {n(x)} 5 V 42 H {n(x+size)} V 5", closed=False))
            elif feature == "tab":
                geometry.append(path(f"M {n(x)} 65 V 35 H {n(x+size)} V 65", closed=False))
            else:
                geometry.append(circle(x + 7, 34, size / 2))
            geometry.append(label(x + 4, 54, f"{size:.2f}", 2.5, "middle"))
        c.add(Asset(asset_id, title,
            f"A seven-step {subtype} series around the configured {thickness:.2f} mm measured material thickness.",
            "calibration", subtype, 210, 70, geometry, fit_type="loose-to-press",
            tags=["calibration", subtype, "fit", "material thickness"], operations=["CUT", "ENGRAVE"],
            parameters={"material_thickness_mm": thickness, "offsets_mm": offsets}))

    gauge("tc-cal-slot-fit", "Slot-fit gauge", "slot-fit", "slot")
    gauge("tc-cal-tab-fit", "Tab-fit gauge", "tab-fit", "tab")
    gauge("tc-cal-hole-fit", "Hole-fit gauge", "hole-fit", "hole")
    gauge("tc-cal-material-thickness", "Material thickness gauge", "thickness", "slot")

    geometry = [rect(5, 5, 160, 60), label(82.5, 13, "LOOSE · SLIP · SNUG · PRESS", 3, "middle")]
    fit_names = ["loose", "slip", "snug", "press"]
    fit_offsets = [0.30, 0.15, 0.00, -0.15]
    for i, (name, offset) in enumerate(zip(fit_names, fit_offsets)):
        x = 22 + i * 36
        size = thickness + offset
        geometry += [path(f"M {n(x)} 5 V 43 H {n(x+size)} V 5", closed=False), label(x+size/2, 53, name, 2.5, "middle"), label(x+size/2, 58, f"{size:.2f} mm", 2.2, "middle")]
    c.add(Asset("tc-cal-four-fit-series", "Loose, slip, snug and press fit series",
        "Four named starting fits for comparison on one measured sheet.", "calibration", "fit-series", 170, 70, geometry,
        fit_type="loose-to-press", tags=["calibration", "loose", "slip", "snug", "press"], operations=["CUT", "ENGRAVE"],
        parameters={"material_thickness_mm": thickness, "fits": dict(zip(fit_names, fit_offsets))}))

    geometry = [rect(5, 5, 110, 25), line(10, 20, 110, 20, "SCORE"), label(60, 10, "100 mm RULER CHECK", 3, "middle")]
    for i in range(101):
        x = 10 + i
        tick = 6 if i % 10 == 0 else 3 if i % 5 == 0 else 1.5
        geometry.append(line(x, 20, x, 20 - tick, "SCORE"))
    c.add(Asset("tc-cal-ruler-check", "100 mm ruler check", "A scored 100 mm reference with millimetre divisions.",
        "calibration", "ruler", 120, 35, geometry, tags=["calibration", "ruler", "scale"], operations=["CUT", "SCORE", "ENGRAVE"],
        tests={"ruler_length_mm": 100}))


def add_size_families(c: Catalogue) -> None:
    for system, values in (("metric", c.cfg["metric_sizes_mm"]), ("imperial", [float(v) * 25.4 for v in c.cfg["imperial_sizes_in"]])):
        originals = values if system == "metric" else c.cfg["imperial_sizes_in"]
        for value, original in zip(values, originals):
            diameter = float(value)
            slug = f"{n(float(original)).replace('.', 'p')}{'mm' if system == 'metric' else 'in'}"
            display = f"{n(diameter)} mm" if system == "metric" else f"{n(float(original))} in ({n(diameter)} mm)"
            canvas = diameter + 10
            params = {"diameter_mm": round(diameter, 4), "size_system": system}
            c.add(Asset(f"tc-disc-{slug}", f"{display} circle", f"An exact-size {display} circular disc outline.",
                "core-geometry", "circles", canvas, canvas, [circle(canvas/2, canvas/2, diameter/2)],
                tags=["circle", "disc", system], parameters=params, tests={"circle_diameter_mm": round(diameter, 4)}))
            plate = max(30, diameter + 16)
            c.add(Asset(f"tc-hole-{slug}", f"{display} circular hole", f"A centred {display} circular hole in a simple test plate.",
                "core-geometry", "circular-holes", plate, plate, [rect(0.5, 0.5, plate-1, plate-1), circle(plate/2, plate/2, diameter/2)],
                tags=["hole", "circle", system], parameters=params, tests={"hole_diameter_mm": round(diameter, 4)}))
    for outer in (20, 30, 40, 50, 75, 100):
        wall = 5 if outer <= 50 else 10
        canvas = outer + 10
        c.add(Asset(f"tc-ring-{outer}mm-wall-{wall}mm", f"{outer} mm ring, {wall} mm wall",
            "A concentric ring/washer with explicit outer diameter and wall thickness.", "core-geometry", "rings-washers",
            canvas, canvas, [circle(canvas/2, canvas/2, outer/2), circle(canvas/2, canvas/2, outer/2-wall)],
            tags=["ring", "washer", "circle"], parameters={"outer_diameter_mm": outer, "wall_mm": wall},
            tests={"outer_diameter_mm": outer, "inner_diameter_mm": outer-2*wall}))


def add_core_geometry(c: Catalogue) -> None:
    for width, height in c.cfg["plate_sizes_mm"]:
        for subtype, rounded in (("rectangles", 0), ("rounded-rectangles", min(8, min(width, height)/6))):
            suffix = "rectangle" if not rounded else "rounded-rectangle"
            c.add(Asset(f"tc-{suffix}-{width}x{height}mm", f"{width} × {height} mm {suffix.replace('-', ' ')}",
                "An exact-size editable plate outline with a millimetre canvas.", "core-geometry", subtype, width, height,
                plate_geometry(width, height, rounded), tags=[suffix, "plate", "exact size"],
                parameters={"width_mm": width, "height_mm": height, "corner_radius_mm": rounded},
                tests={"plate_width_mm": width, "plate_height_mm": height}))
        border = 8
        c.add(Asset(f"tc-frame-{width}x{height}mm", f"{width} × {height} mm frame",
            "A rectangular frame with a consistent editable border.", "core-geometry", "frames", width, height,
            [rect(0, 0, width, height), rect(border, border, width-2*border, height-2*border)],
            tags=["frame", "rectangle"], parameters={"width_mm": width, "height_mm": height, "border_mm": border}))

    specials = [
        Asset("tc-ellipse-80x50mm", "80 × 50 mm ellipse", "An exact-size ellipse outline.", "core-geometry", "ellipses", 90, 60, [ellipse(45,30,40,25)], tags=["ellipse"], tests={"ellipse_width_mm":80,"ellipse_height_mm":50}),
        Asset("tc-capsule-100x30mm", "100 × 30 mm capsule", "A capsule/obround made as one rounded rectangle.", "core-geometry", "capsules", 110, 40, [rect(5,5,100,30,rx=15)], tags=["capsule","obround"], tests={"capsule_width_mm":100,"capsule_height_mm":30}),
        Asset("tc-triangle-equilateral-75mm", "75 mm equilateral triangle", "An editable equilateral triangle outline.", "core-geometry", "triangles", 85, 75, [polygon([(5,69.95),(42.5,5),(80,69.95)])], tags=["triangle","polygon"]),
        Asset("tc-polygon-hexagon-60mm", "60 mm hexagon", "A regular six-sided polygon.", "core-geometry", "polygons", 70,70,[polygon(regular_polygon(35,35,30,6))], tags=["hexagon","polygon"]),
        Asset("tc-polygon-octagon-60mm", "60 mm octagon", "A regular eight-sided polygon.", "core-geometry", "polygons", 70,70,[polygon(regular_polygon(35,35,30,8))], tags=["octagon","polygon"]),
        Asset("tc-star-five-point-60mm", "60 mm five-point star", "An original procedural five-point star outline.", "core-geometry", "stars", 70,70,[polygon(star_points(35,35,30,12))], tags=["star","polygon"]),
        Asset("tc-slot-40x6mm", "40 × 6 mm slot", "A simple closed rectangular slot test plate.", "core-geometry", "slots", 70,35,[rect(0.5,0.5,69,34),rect(15,14.5,40,6)], tags=["slot","fit"], fit_type="configurable", parameters={"slot_width_mm":6,"slot_length_mm":40}),
        Asset("tc-rounded-slot-40x6mm", "40 × 6 mm rounded slot", "A closed slot with semicircular ends.", "core-geometry", "rounded-slots", 70,35,[rect(0.5,0.5,69,34),rect(15,14.5,40,6,rx=3)], tags=["rounded slot","fit"], fit_type="configurable"),
        Asset("tc-u-slot-30x8mm", "30 × 8 mm U-slot", "An open-ended U-slot starter for measured retention geometry.", "core-geometry", "u-slots", 60,50,[rect(0.5,0.5,59,49),path("M 26 0.5 V 31 Q 30 35 34 31 V 0.5",closed=False)], tags=["U-slot","retention"], fit_type="configurable"),
        Asset("tc-v-notch-20x15mm", "20 × 15 mm V-notch", "An open V-notch starter in a simple plate.", "core-geometry", "v-notches", 60,50,[rect(0.5,0.5,59,49),path("M 20 0.5 L 30 15.5 L 40 0.5",closed=False)], tags=["V-notch","retention"]),
        Asset("tc-keyhole-12x24mm", "12 × 24 mm keyhole", "A generic keyhole mounting opening for prototyping only.", "core-geometry", "keyholes", 45,45,[rect(0.5,0.5,44,44),path("M 22.5 9 A 6 6 0 1 1 22.5 21 L 25.5 34 H 19.5 L 22.5 21 A 6 6 0 0 1 22.5 9 Z")], tags=["keyhole","mounting"]),
        Asset("tc-gusset-right-75mm", "75 mm right-triangle gusset", "A generic right-triangle gusset blank.", "core-geometry", "gussets", 80,80,[polygon([(2.5,2.5),(77.5,77.5),(2.5,77.5)])], tags=["gusset","triangle"]),
        Asset("tc-bracket-l-100mm", "100 mm L-bracket blank", "A flat laminated L-bracket starter profile.", "core-geometry", "brackets", 110,110,[path("M 5 5 H 35 V 75 H 105 V 105 H 5 Z")], tags=["bracket","laminated"]),
        Asset("tc-spacer-30mm-m6", "30 mm spacer with M6 clearance", "A circular spacer for laminated assemblies.", "core-geometry", "spacers", 40,40,[circle(20,20,15),circle(20,20,3.3)], tags=["spacer","M6","lamination"]),
        Asset("tc-label-plate-100x30mm", "100 × 30 mm label plate", "A rounded label plate with two mounting holes and a score guide.", "core-geometry", "label-plates", 100,30,[rect(0.5,0.5,99,29,rx=5),circle(8,15,2),circle(92,15,2),line(20,20,80,20),label(50,14,"LABEL",4,"middle")], tags=["label plate","sign"], operations=["CUT","SCORE","ENGRAVE"]),
        Asset("tc-zip-tie-pattern-4mm", "4 mm zip-tie mounting pattern", "A generic two-slot zip-tie mounting pattern.", "core-geometry", "zip-tie-patterns", 60,35,[rect(0.5,0.5,59,34),rect(16,14,10,4,rx=2),rect(34,14,10,4,rx=2)], tags=["zip tie","cable","mounting"]),
        Asset("tc-hook-utility-small", "Small generic utility hook profile", "A laminated hook starter; load testing is required.", "core-geometry", "hooks", 80,70,[path("M 5 5 H 30 V 40 H 55 V 20 H 75 V 60 H 20 V 20 H 5 Z")], tags=["hook","holder","laminated"], skill_level="intermediate", notes="Prototype only. Verify laminate, fasteners, retention, centre of mass and safe load before use."),
        Asset("tc-tabs-three-widths", "Three tab starter widths", "A plate with 10, 15 and 20 mm external tab starters.", "core-geometry", "tabs", 90,50,[path("M 5 5 H 85 V 45 H 65 V 50 H 45 V 45 H 30 V 50 H 15 V 45 H 5 Z")], tags=["tab","joinery"], fit_type="configurable")
    ]
    for asset in specials:
        c.add(asset)

    for spec in c.cfg["hole_patterns"]:
        sx, sy, hole = float(spec["spacing_x_mm"]), float(spec["spacing_y_mm"]), float(spec["hole_mm"])
        width, height = sx + 20, sy + 20
        geometry = [rect(0.5,0.5,width-1,height-1)]
        for x in (10, 10+sx):
            for y in (10, 10+sy):
                geometry.append(circle(x,y,hole/2))
        c.add(Asset(f"tc-mount-{spec['name']}", spec["name"].replace("-"," ").title(),
            "A generic four-hole mounting pattern; verify the target hardware before cutting.", "core-geometry", "mounting-patterns",
            width,height,geometry,shop="electronics" if "fan" in spec["name"] else "general", tool_family="mounting",
            tags=["mounting pattern",spec["name"]], parameters=dict(spec), tests={"spacing_x_mm":sx,"spacing_y_mm":sy,"hole_diameter_mm":hole}))

    geometry = [circle(60,60,55), circle(60,60,3)]
    for i in range(12):
        a = i*math.pi/6
        geometry.append(circle(60+45*math.cos(a),60+45*math.sin(a),2.5))
    c.add(Asset("tc-bolt-circle-90mm-12x5mm", "90 mm bolt circle, 12 × 5 mm holes",
        "A twelve-hole bolt-circle template with a centre reference.", "core-geometry", "bolt-circles", 120,120,geometry,
        tags=["bolt circle","mounting","drill template"], parameters={"pitch_circle_diameter_mm":90,"hole_count":12,"hole_diameter_mm":5}))


def add_french_cleat(c: Catalogue) -> None:
    for width, height in c.cfg["modular_faces_mm"]:
        geometry = [rect(0,0,width,height,rx=3), circle(12,12,2.6), circle(width-12,12,2.6),
                    line(10,30,width-10,30,"SCORE"), label(width/2,22,f"MODULE {width} × {height} mm",4,"middle")]
        c.add(Asset(f"tc-cleat-module-face-{width}x{height}mm", f"French-cleat module face {width} × {height} mm",
            "A standard blank module face with mounting references and label area.", "french-cleat", "module-faces",
            width,height,geometry,tool_family="modular organization",tags=["French cleat","module face","shadow board"],
            operations=["CUT","SCORE","ENGRAVE"], parameters={"face_width_mm":width,"face_height_mm":height},
            notes="Face size is not a load rating. Use an appropriate solid cleat/backer and approved fasteners."))
    accessories = [
        ("interface-300", "Cleat interface reference", 300, 60, [rect(0.5,0.5,299,59), line(0.5,30,299.5,30,"SCORE")]),
        ("module-cleat-200", "Module cleat strip", 200, 45, [path("M 0.5 0.5 H 199.5 V 44.5 H 18 L 0.5 27 Z")]),
        ("double-cleat-backer-300", "Double-cleat backer", 300, 150, [rect(0.5,0.5,299,149),line(10,40,290,40,"SCORE"),line(10,110,290,110,"SCORE")]),
        ("lower-standoff-150", "Lower standoff strip", 150, 25, [rect(0.5,0.5,149,24)]),
        ("anti-slide-stop", "Anti-slide stop pair", 80, 35, [rect(5,5,30,25),rect(45,5,30,25)]),
        ("anti-lift-retainer", "Anti-lift retainer prototype", 100, 45, [path("M 5 5 H 95 V 20 H 65 V 40 H 35 V 20 H 5 Z")]),
        ("alignment-jig", "French-cleat alignment jig", 220, 80, [rect(0.5,0.5,219,79),line(10,20,210,20,"SCORE"),line(10,60,210,60,"SCORE"),label(110,43,"40.00 mm RAIL REFERENCE",4,"middle")]),
        ("drilling-template", "French-cleat drilling template", 300, 60, [rect(0.5,0.5,299,59)]+[circle(x,30,2) for x in range(25,300,50)]),
        ("pegboard-adapter", "Pegboard-to-cleat concept plate", 200, 100, [rect(0.5,0.5,199,99)]+[circle(x,y,3) for x in (25,50,75,100,125,150,175) for y in (25,50,75)]),
        ("blank-shelf", "Blank module shelf parts", 240, 170, [rect(5,5,150,80),rect(5,90,150,70),polygon([(165,5),(235,80),(165,80)]),polygon([(165,90),(235,165),(165,165)])]),
        ("cable-module", "Cable and cord module", 200, 120, [rect(0.5,0.5,199,119)]+[path(f"M {x} 0.5 V 38 Q {x+5} 44 {x+10} 38 V 0.5",closed=False) for x in range(20,181,30)])
    ]
    for aid,title,width,height,geometry in accessories:
        operations = sorted({op for op in ("CUT","SCORE","ENGRAVE") if any(f'data-operation="{op}"' in g for g in geometry)})
        c.add(Asset(f"tc-cleat-{aid}",title,"A configurable component in the removable French-cleat organization ecosystem.",
            "french-cleat","interfaces-accessories",width,height,geometry,tool_family="modular organization",
            tags=["French cleat",title.lower(),"organization"],operations=operations,skill_level="intermediate",
            notes="Prototype only. Thin laser-cut plywood is not a substitute for a structural rail. Verify wall, fasteners, backing, load and anti-lift retention."))


def add_holders(c: Catalogue) -> None:
    material_thickness = float(c.cfg["default_material"]["measured_thickness_mm"])
    for spec in c.cfg["holder_families"]:
        count, diameter, spacing = int(spec["count"]), float(spec["diameter_mm"]), float(spec["spacing_mm"])
        rack_width = max(100, 30 + (count-1)*spacing + diameter)
        width, height = rack_width + 72, 160
        geometry = [
            # Labelled back plate with two mounting holes.
            rect(5, 5, rack_width, 55, rx=3),
            circle(17, 17, 2.6),
            circle(5 + rack_width - 12, 17, 2.6),
            label(5 + rack_width / 2, 26, spec["title"].upper(), 4, "middle"),
            label(5 + rack_width / 2, 38, "MEASURE · TEST FIT · ASSEMBLE", 2.5, "middle"),
            # Horizontal retention deck and front rail.
            rect(5, 70, rack_width, 45, rx=2),
            rect(5, 126, rack_width, 18, rx=2),
            # Two right-triangle cheeks support the deck as a three-dimensional rack.
            polygon([(rack_width + 17, 5), (rack_width + 67, 5), (rack_width + 17, 55)]),
            polygon([(rack_width + 17, 68), (rack_width + 67, 68), (rack_width + 17, 118)]),
            label(rack_width + 42, 127, "2 × CHEEKS", 2.3, "middle"),
        ]
        start = 5 + (rack_width-(count-1)*spacing)/2
        for i in range(count):
            x = start+i*spacing
            if spec["retention"] == "hole-array":
                geometry.append(circle(x,92,diameter/2))
            else:
                geometry.append(path(f"M {n(x-diameter/2)} 115 V 92 Q {n(x)} 86 {n(x+diameter/2)} 92 V 115",closed=False))
        parameters = dict(spec)
        parameters.update({
            "rack_width_mm": rack_width,
            "material_thickness_mm": material_thickness,
            "components": ["back-plate", "retention-deck", "front-rail", "left-cheek", "right-cheek"],
        })
        c.add(Asset(f"tc-holder-{spec['id']}", f"{spec['title']} kit",
            "A five-part benchtop rack kit with a labelled back plate, horizontal retention deck, front rail and two support cheeks.",
            "tool-holders",spec["retention"],width,height,geometry,shop=spec["shop"],tool_family=spec["id"],
            tags=[spec["title"].lower(),spec["shop"],"holder","rack kit","benchtop","laminated assembly"],skill_level="intermediate",
            operations=["CUT","ENGRAVE"],parameters=parameters,
            notes="Glue the deck and front rail between the support cheeks and back plate. Measure the actual tools, verify removal clearance and centre of mass, then prototype and load-test before wall mounting."))

    # `shop_coverage` is a requirements backlog, not permission to publish a
    # renamed generic plate for every tool name. Only reviewed holder families
    # with explicit retention parameters are emitted above.


def add_jigs_gauges(c: Catalogue) -> None:
    """Add purpose-built measuring and setup tools with distinct geometry."""

    def add_jig(
        asset_id: str,
        title: str,
        description: str,
        subcategory: str,
        width: float,
        height: float,
        geometry: list[str],
        *,
        parameters: dict[str, Any],
        tests: dict[str, float] | None = None,
        notes: str,
    ) -> None:
        operations = [
            operation for operation in ("CUT", "SCORE", "ENGRAVE")
            if any(f'data-operation="{operation}"' in item for item in geometry)
        ]
        c.add(Asset(
            f"tc-jig-{asset_id}", title, description, "jigs-gauges", subcategory,
            width, height, geometry, shop="general", tool_family=subcategory,
            tags=["jig", "gauge", subcategory, *asset_id.split("-")],
            operations=operations, parameters=parameters, tests=tests or {}, notes=notes,
        ))

    radii = [2, 4, 6, 8, 10, 15, 20]
    geometry = [label(90, 8, "EXTERNAL CORNER RADIUS LEAVES", 3.5, "middle")]
    for index, radius in enumerate(radii):
        row, column = divmod(index, 4)
        x, y = 4 + column * 44, 14 + row * 42
        geometry.append(path(
            f"M {n(x)} {n(y)} H {n(x + 40 - radius)} "
            f"A {n(radius)} {n(radius)} 0 0 1 {n(x + 40)} {n(y + radius)} "
            f"V {n(y + 36)} H {n(x)} Z"
        ))
        geometry.append(label(x + 20, y + 30, f"R{radius}", 2.5, "middle"))
    add_jig(
        "radius-gauge", "External radius gauge leaves R2–R20",
        "Seven separate corner leaves with true tangent arcs for comparing an outside corner radius.",
        "radius-gauges", 180, 100, geometry,
        parameters={"radii_mm": radii, "profile": "convex-quarter-circle"},
        tests={"smallest_radius_mm": 2, "largest_radius_mm": 20},
        notes="Cut as separate leaves. Compare by backlighting the contact edge; this is a shop reference, not an inspection-certified gauge.",
    )

    angles = [15, 30, 45, 60, 75, 90]
    centre_x, centre_y, ray_length = 90, 88, 68
    geometry = [rect(0.5, 0.5, 179, 99, rx=3), label(90, 10, "ANGLE REFERENCE — ALIGN TO BASELINE", 3.4, "middle")]
    geometry.append(line(15, centre_y, 165, centre_y, "SCORE"))
    for angle in angles:
        radians = math.radians(angle)
        end_x = centre_x + ray_length * math.cos(radians)
        end_y = centre_y - ray_length * math.sin(radians)
        geometry.append(line(centre_x, centre_y, end_x, end_y, "SCORE"))
        geometry.append(label(
            centre_x + (ray_length + 8) * math.cos(radians),
            centre_y - (ray_length + 8) * math.sin(radians),
            f"{angle}°", 2.4, "middle",
        ))
    add_jig(
        "angle-gauge", "Angle reference 15°–90°",
        "A common-vertex angle fan with a scored baseline and six exact reference rays.",
        "angle-gauges", 180, 100, geometry,
        parameters={"angles_deg": angles, "ray_length_mm": ray_length},
        tests={"largest_angle_deg": 90},
        notes="Align one workpiece edge to the horizontal datum and compare the second edge to a scored ray.",
    )

    geometry = [rect(0.5, 0.5, 159, 109, rx=3), label(80, 10, "CIRCLE CENTRE FINDER", 3.5, "middle")]
    centre_x, centre_y = 80, 60
    geometry += [circle(centre_x, centre_y, 2), line(12, centre_y, 148, centre_y, "SCORE"),
                 line(centre_x, 18, centre_x, 102, "SCORE"), line(35, 15, 125, 105, "SCORE"),
                 line(35, 105, 125, 15, "SCORE")]
    for radius in (10, 20, 30, 40):
        geometry.append(circle(centre_x, centre_y, radius, "SCORE"))
        geometry.append(label(centre_x + radius + 1.5, centre_y - 1.5, f"Ø{radius * 2}", 2.1))
    add_jig(
        "centering-template", "Circle centering template",
        "Crosshairs, diagonals and concentric scored circles locate the centre of round work up to 80 mm diameter.",
        "centering", 160, 110, geometry,
        parameters={"reference_diameters_mm": [20, 40, 60, 80], "centre_hole_mm": 4},
        tests={"largest_reference_diameter_mm": 80, "centre_hole_diameter_mm": 4},
        notes="Use the scored references to align the work, then mark through the 4 mm centre hole.",
    )

    spacings = [10, 20, 30, 40, 50]
    geometry = [rect(0.5, 0.5, 209, 109, rx=3), label(105, 10, "DRILL SPACING — CENTRE TO CENTRE", 3.4, "middle")]
    for index, spacing in enumerate(spacings):
        y, x1 = 26 + index * 17, 40
        x2 = x1 + spacing
        geometry += [circle(x1, y, 1.5), circle(x2, y, 1.5), line(x1, y, x2, y, "SCORE"),
                     label(105, y + 1, f"{spacing} mm C-C", 2.6, "middle")]
    add_jig(
        "drill-spacing", "Drill spacing template 10–50 mm",
        "Five labelled pairs of 3 mm pilot holes set exact centre-to-centre spacing.",
        "drill-spacing", 210, 110, geometry,
        parameters={"spacings_mm": spacings, "pilot_hole_mm": 3},
        tests={"minimum_spacing_mm": 10, "maximum_spacing_mm": 50},
        notes="Insert a transfer punch or mark through both pilot holes; compensate for kerf after a test cut.",
    )

    fasteners = [3, 4, 5, 6, 8, 10, 12]
    geometry = [rect(0.5, 0.5, 209, 87, rx=3), label(105, 10, "METRIC FASTENER SHANK SIZING", 3.4, "middle")]
    for index, size in enumerate(fasteners):
        x = 20 + index * 28
        geometry += [circle(x, 42, size / 2), label(x, 62, f"M{size}", 2.8, "middle"),
                     label(x, 69, f"Ø{size} mm", 2.1, "middle")]
    add_jig(
        "fastener-sizing", "Metric fastener shank sizing board",
        "A labelled M3–M12 through-hole board for identifying nominal metric fastener shank diameter.",
        "fastener-sizing", 210, 88, geometry,
        parameters={"nominal_metric_sizes": fasteners, "hole_diameters_mm": fasteners},
        tests={"smallest_hole_diameter_mm": 3, "largest_hole_diameter_mm": 12},
        notes="Hole size is kerf-sensitive. Test-cut and measure the finished holes before using the board as a reference.",
    )

    geometry = [rect(0.5, 0.5, 179, 69, rx=3), label(90, 9, "SCREW LENGTH — UNDER HEAD TO TIP", 3.4, "middle")]
    zero_x, scale_y, scale_length = 25, 53, 120
    geometry += [line(zero_x, 18, zero_x, 58, "SCORE"), line(zero_x, scale_y, zero_x + scale_length, scale_y, "SCORE"),
                 label(zero_x - 2, 17, "HEAD DATUM", 2.2, "end")]
    for millimetre in range(scale_length + 1):
        x = zero_x + millimetre
        tick = 8 if millimetre % 10 == 0 else 5 if millimetre % 5 == 0 else 2.5
        geometry.append(line(x, scale_y, x, scale_y - tick, "SCORE"))
        if millimetre % 10 == 0:
            geometry.append(label(x, 64, str(millimetre), 2.2, "middle"))
    geometry.append(label(zero_x + scale_length + 6, 64, "mm", 2.2))
    add_jig(
        "screw-length", "Screw length gauge 0–120 mm",
        "A linear under-head datum and millimetre scale for measuring screw length—not screw diameter.",
        "screw-length", 180, 70, geometry,
        parameters={"measurement_axis": "under-head-to-tip", "scale_length_mm": scale_length, "minor_division_mm": 1},
        tests={"scale_length_mm": scale_length, "minor_division_mm": 1},
        notes="Seat the underside of the screw head on the vertical zero datum and read the tip against the engraved scale.",
    )

    drill_sizes = list(range(3, 13))
    geometry = [rect(0.5, 0.5, 229, 81, rx=3), label(115, 10, "METRIC DRILL SHANK CHECK", 3.4, "middle")]
    for index, size in enumerate(drill_sizes):
        x = 17 + index * 22
        geometry += [circle(x, 39, size / 2), label(x, 62, f"Ø{size}", 2.5, "middle")]
    add_jig(
        "drill-size", "Metric drill-size gauge Ø3–12 mm",
        "Ten sequential through-holes identify common metric drill-shank diameters from 3 to 12 mm.",
        "drill-size", 230, 82, geometry,
        parameters={"hole_diameters_mm": drill_sizes, "increment_mm": 1},
        tests={"smallest_hole_diameter_mm": 3, "largest_hole_diameter_mm": 12},
        notes="Laser kerf changes the finished holes. Measure a physical test cut and record the correction before shop use.",
    )

    wrench_sizes = [6, 7, 8, 10, 12, 13, 14, 15, 17, 19]
    geometry = [rect(0.5, 0.5, 229, 109, rx=3), label(115, 10, "HEX / NUT ACROSS-FLATS CHECK", 3.4, "middle")]
    for index, size in enumerate(wrench_sizes):
        row, column = divmod(index, 5)
        x, y = 24 + column * 45, 31 + row * 42
        geometry += [rect(x - size / 2, y, size, 15, rx=1), label(x, y + 23, f"{size} mm", 2.4, "middle")]
    add_jig(
        "wrench-size", "Metric wrench-size gauge 6–19 mm",
        "Ten exact-width slots compare the across-flats dimension of metric hex heads and nuts.",
        "wrench-size", 230, 110, geometry,
        parameters={"slot_widths_mm": wrench_sizes, "reference": "hex-across-flats"},
        tests={"smallest_slot_width_mm": 6, "largest_slot_width_mm": 19},
        notes="Use only after measuring kerf compensation; this reference does not replace a wrench or caliper.",
    )

    wire_sizes = [0.5, 0.8, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0]
    geometry = [rect(0.5, 0.5, 209, 89, rx=3), label(105, 10, "CABLE / WIRE OUTSIDE DIAMETER", 3.4, "middle")]
    for index, size in enumerate(wire_sizes):
        x = 16 + index * 22
        geometry += [path(f"M {n(x - size / 2)} 89 V 42 H {n(x + size / 2)} V 89", closed=False),
                     label(x, 33, f"{n(size)}", 2.4, "middle")]
    geometry.append(label(105, 78, "OPEN SLOTS · VALUES IN mm", 2.4, "middle"))
    add_jig(
        "cable-wire", "Cable and wire outside-diameter gauge",
        "Nine open-edge slots compare cable or insulated-wire outside diameter from 0.5 to 6 mm.",
        "cable-wire", 210, 90, geometry,
        parameters={"slot_widths_mm": wire_sizes, "measurement": "outside-diameter"},
        tests={"smallest_slot_width_mm": 0.5, "largest_slot_width_mm": 6},
        notes="Do not force conductors into a slot. Deburr the cut edges and verify slot width after kerf compensation.",
    )

    block_heights = [10, 20, 30, 40, 50]
    geometry = [label(90, 8, "SEPARATE SETUP BLOCKS", 3.5, "middle")]
    for index, block_height in enumerate(block_heights):
        x, y = 6 + index * 34, 68 - block_height
        geometry += [rect(x, y, 28, block_height, rx=1),
                     label(x + 14, max(y + 7, 14), f"{block_height} mm", 2.5, "middle")]
    add_jig(
        "setup-block", "Setup block set 10–50 mm",
        "Five separate rectangular setup blocks whose physical heights are 10, 20, 30, 40 and 50 mm.",
        "setup-blocks", 180, 72, geometry,
        parameters={"block_heights_mm": block_heights, "block_width_mm": 28},
        tests={"smallest_block_height_mm": 10, "largest_block_height_mm": 50},
        notes="Measure the finished blocks with calipers before using them to position work or machinery.",
    )

    sanding_radii = [5, 10, 15, 20, 25, 30]
    geometry = [label(110, 8, "QUARTER-ROUND SANDING PROFILES", 3.5, "middle")]
    for index, radius in enumerate(sanding_radii):
        row, column = divmod(index, 3)
        x, y = 10 + column * 70, 15 + row * 53
        geometry.append(path(f"M {n(x)} {n(y)} H {n(x + radius)} A {radius} {radius} 0 0 1 {n(x)} {n(y + radius)} Z"))
        geometry.append(label(x + 33, y + min(radius, 25), f"R{radius}", 2.5))
    add_jig(
        "sanding-radius", "Quarter-round sanding profiles R5–R30",
        "Six separate quarter-circle profiles provide exact convex forms for checking or backing an inside radius.",
        "sanding-radius", 220, 120, geometry,
        parameters={"radii_mm": sanding_radii, "profile": "quarter-circle"},
        tests={"smallest_radius_mm": 5, "largest_radius_mm": 30},
        notes="Laminate pieces when a wider sanding block is needed; verify the finished arc before use.",
    )

    pitch = 2.54
    columns, rows = 20, 10
    start_x, start_y = 24, 25
    geometry = [rect(0.5, 0.5, 139, 69, rx=3), label(70, 10, "PCB 2.54 mm / 0.1 in PITCH", 3.4, "middle")]
    for column in range(columns):
        for row in range(rows):
            geometry.append(circle(start_x + column * pitch, start_y + row * pitch, 0.45))
    geometry += [line(start_x, 58, start_x + 10 * pitch, 58, "SCORE"),
                 label(start_x + 5 * pitch, 65, "10 pitches = 25.4 mm", 2.3, "middle")]
    add_jig(
        "pcb-spacing", "PCB pitch template 2.54 mm (0.1 in)",
        "A 20 × 10 through-hole grid on true 2.54 mm pitch with a ten-pitch dimensional reference.",
        "pcb-spacing", 140, 70, geometry,
        parameters={"pitch_mm": pitch, "columns": columns, "rows": rows, "hole_diameter_mm": 0.9},
        tests={"pitch_mm": pitch, "ten_pitch_span_mm": 25.4},
        notes="This is a layout reference. Verify the 25.4 mm ten-pitch span after cutting before aligning electronics hardware.",
    )

    slot_widths = [3, 4, 5, 6, 8, 10, 12]
    geometry = [rect(0.5, 0.5, 209, 89, rx=3), label(105, 10, "SLOT WIDTH CHECK", 3.4, "middle")]
    for index, width in enumerate(slot_widths):
        x = 18 + index * 29
        geometry += [rect(x - width / 2, 30, width, 28, rx=width / 2),
                     label(x, 70, f"{width} mm", 2.4, "middle")]
    add_jig(
        "slot-width", "Slot-width gauge 3–12 mm",
        "Seven cut slots provide direct physical checks of finished slot width after kerf compensation.",
        "slot-gauges", 210, 90, geometry,
        parameters={"slot_widths_mm": slot_widths},
        tests={"smallest_slot_width_mm": 3, "largest_slot_width_mm": 12},
        notes="Measure the fabricated slots; nominal SVG width is not proof of finished width on a laser cutter.",
    )

    bolt_circles = [20, 30, 40]
    geometry = [rect(0.5, 0.5, 179, 99, rx=3), label(90, 10, "FOUR-HOLE BOLT CIRCLES", 3.4, "middle")]
    for index, diameter in enumerate(bolt_circles):
        cx, cy, radius = 35 + index * 55, 53, diameter / 2
        geometry += [circle(cx, cy, radius, "SCORE"), circle(cx, cy, 1.5)]
        for angle in (0, 90, 180, 270):
            radians = math.radians(angle)
            geometry.append(circle(cx + radius * math.cos(radians), cy + radius * math.sin(radians), 1.5))
        geometry.append(label(cx, 88, f"PCD {diameter}", 2.4, "middle"))
    add_jig(
        "bolt-circle", "Four-hole bolt-circle templates PCD 20–40 mm",
        "Three four-hole patterns place 3 mm pilot holes on exact 20, 30 and 40 mm pitch-circle diameters.",
        "bolt-circle", 180, 100, geometry,
        parameters={"pitch_circle_diameters_mm": bolt_circles, "hole_count": 4, "pilot_hole_mm": 3},
        tests={"smallest_pcd_mm": 20, "largest_pcd_mm": 40},
        notes="Use transfer punches through the pilot holes; confirm centre distances after the first cut.",
    )

    shelf_pitch, shelf_count = 32, 7
    geometry = [rect(0.5, 0.5, 69, 239, rx=3), label(8, 120, "32 mm SYSTEM", 3.2, "middle")]
    hole_x, first_y = 37, 22
    geometry += [line(hole_x, 14, hole_x, 224, "SCORE"), line(0.5, 14, 69.5, 14, "SCORE")]
    for index in range(shelf_count):
        y = first_y + index * shelf_pitch
        geometry += [circle(hole_x, y, 2.5), label(48, y + 1, str(index * shelf_pitch), 2.2)]
    add_jig(
        "shelf-spacing", "32 mm shelf-hole spacing template",
        "A vertical seven-hole template on 32 mm pitch with a 37 mm edge setback reference.",
        "shelf-spacing", 70, 240, geometry,
        parameters={"pitch_mm": shelf_pitch, "hole_count": shelf_count, "edge_setback_mm": 37, "hole_diameter_mm": 5},
        tests={"pitch_mm": shelf_pitch, "edge_setback_mm": 37},
        notes="Clamp to a verified cabinet edge and use an appropriate drill guide; the laser-cut part is a layout template, not a precision bushing.",
    )


def add_jigs_projects_themes(c: Catalogue) -> None:
    thickness=float(c.cfg["default_material"]["measured_thickness_mm"]); clearance=float(c.cfg["fabrication"]["clearance_mm"]); slot=thickness+clearance
    projects = [
        ("sign-blank", "Rounded sign blank", 200,100,[rect(0.5,0.5,199,99,rx=8),circle(15,15,2.5),circle(185,15,2.5)]),
        ("plaque-blank", "Plaque blank", 180,90,[path("M 10 0.5 H 170 Q 179.5 0.5 179.5 10 V 80 Q 179.5 89.5 170 89.5 H 10 Q 0.5 89.5 0.5 80 V 10 Q 0.5 0.5 10 0.5 Z")]),
        ("tag-blank", "Tag blank", 80,40,[path("M 0.5 8 L 8 0.5 H 79.5 V 39.5 H 8 L 0.5 32 Z"),circle(10,20,2.5)]),
        ("keychain-blank", "Keychain blank", 70,30,[rect(0.5,0.5,69,29,rx=8),circle(9,15,2.5)]),
        ("bookmark-blank", "Bookmark blank", 45,160,[rect(0.5,0.5,44,159,rx=3),circle(22.5,12,3)]),
        ("coaster-blank", "Coaster blank", 100,100,[rect(0.5,0.5,99,99,rx=8)]),
        ("straight-leg", "Straight project leg", 50,160,[rect(0.5,0.5,49,159,rx=3)]),
        ("angled-leg", "Angled project leg", 70,160,[polygon([(0.5,0.5),(45,0.5),(69.5,159.5),(20,159.5)])]),
        ("t-foot", "T-foot stand components", 180,100,[rect(5,5,80,35),rect(95,5,80,35),rect(50,55,80,35),rect(42,5+17.5-slot/2,slot,17.5),rect(128,55,slot,35)]),
        ("cross-stand", "Cross stand pair", 180,100,[rect(5,5,80,90),rect(95,5,80,90),rect(42.5-slot/2,5,slot,45),rect(132.5-slot/2,50,slot,45)]),
        ("easel-starter", "Easel starter parts", 220,180,[polygon([(5,175),(70,5),(135,175)]),rect(145,20,65,18),rect(145,55,65,110)]),
        ("divider-panel", "Tray divider panel", 150,80,[rect(0.5,0.5,149,79),rect(75-slot/2,40,slot,39.5)]),
        ("box-panel", "Simple box panel starter", 150,100,[rect(0.5,0.5,149,99),line(10,15,140,15,"SCORE"),line(10,85,140,85,"SCORE")]),
        ("tab-slot-joint", "Tab-and-slot test pair", 180,80,[rect(5,5,75,70),rect(100,5,75,70),rect(80-slot,30,slot,20),rect(100,30,slot,20)]),
        ("half-lap-joint", "Cross-lap test pair", 180,80,[rect(5,5,75,70),rect(100,5,75,70),rect(42.5-slot/2,5,slot,35),rect(137.5-slot/2,40,slot,35)])
    ]
    for aid,title,width,height,geometry in projects:
        operations=["CUT"] + (["SCORE"] if any('data-operation="SCORE"' in g for g in geometry) else [])
        c.add(Asset(f"tc-project-{aid}",title,"Starting geometry for student measurement, combination and original design work.",
            "project-components",aid,width,height,geometry,shop="general",tool_family="student project",tags=["project component",aid,"starter geometry"],
            fit_type="configurable" if any(term in aid for term in ("stand","joint","foot","divider","panel")) else "none",
            operations=operations,parameters={"material_thickness_mm":thickness,"clearance_mm":clearance} if "configurable" else {}))

    themes = [
        ("winter-snowflake", "Procedural winter snowflake", [line(50,10,50,90,"CUT"),line(15.4,30,84.6,70,"CUT"),line(15.4,70,84.6,30,"CUT")], "seasonal", "none"),
        ("celebration-star-ornament", "Five-point celebration ornament", [polygon(star_points(50,52,40,18)),circle(50,10,2.5)], "celebration", "none"),
        ("heart-tag", "Heart-shaped gift tag", [path("M 50 88 C 15 65 5 45 15 25 C 25 5 45 15 50 28 C 55 15 75 5 85 25 C 95 45 85 65 50 88 Z"),circle(50,18,2.5)], "celebration", "none"),
        ("school-gear", "Generic school technology gear", [circle(50,50,38),circle(50,50,20)]+[rect(46,2,8,14) for _ in range(1)], "school", "none"),
        ("science-atom", "Generic science atom engraving outline", [ellipse(50,50,40,15),ellipse(50,50,15,40),circle(50,50,3)], "science", "none"),
        ("music-note", "Generic music-note starter", [circle(35,75,10),circle(70,65,10),line(45,75,45,25,"CUT"),line(80,65,80,15,"CUT"),line(45,25,80,15,"CUT")], "music", "none"),
        ("space-rocket", "Generic space rocket starter", [path("M 50 5 C 75 25 75 60 60 78 L 40 78 C 25 60 25 25 50 5 Z"),circle(50,42,8),polygon([(40,70),(22,90),(43,82)]),polygon([(60,70),(78,90),(57,82)])], "space", "none"),
        ("safety-glasses", "Generic safety-glasses icon", [circle(32,52,18),circle(68,52,18),line(50,50,50,50.1,"SCORE"),line(50,48,50,48.1,"SCORE")], "safety", "none"),
        ("generic-sport-shield", "Generic sport crest blank", [path("M 15 10 H 85 V 50 C 85 75 65 88 50 95 C 35 88 15 75 15 50 Z")], "sports", "none"),
        ("festival-lantern-blank", "Festival lantern decoration blank", [path("M 30 20 Q 50 5 70 20 V 75 Q 50 90 30 75 Z"),line(30,35,70,35,"SCORE"),line(30,60,70,60,"SCORE")], "cultural celebration", "review-recommended"),
        ("christmas-tree", "Generic Christmas tree starter", [polygon([(50,8),(70,38),(62,38),(82,68),(58,68),(58,90),(42,90),(42,68),(18,68),(38,38),(30,38)]),circle(50,14,2.5)], "Christmas", "review-recommended"),
        ("hanukkah-tag", "Hanukkah design-research tag", [rect(10,20,80,60,rx=8),circle(20,30,2.5),label(50,53,"HANUKKAH",5,"middle")], "Hanukkah", "review-recommended"),
        ("diwali-tag", "Diwali design-research tag", [rect(10,20,80,60,rx=8),circle(20,30,2.5),label(50,53,"DIWALI",5,"middle")], "Diwali", "review-recommended"),
        ("eid-tag", "Eid design-research tag", [rect(10,20,80,60,rx=8),circle(20,30,2.5),label(50,53,"EID",5,"middle")], "Eid", "review-recommended"),
        ("ramadan-tag", "Ramadan design-research tag", [rect(10,20,80,60,rx=8),circle(20,30,2.5),label(50,53,"RAMADAN",5,"middle")], "Ramadan", "review-recommended"),
        ("vaisakhi-tag", "Vaisakhi design-research tag", [rect(10,20,80,60,rx=8),circle(20,30,2.5),label(50,53,"VAISAKHI",5,"middle")], "Vaisakhi", "review-recommended"),
        ("lunar-new-year-lantern", "Lunar New Year lantern starter", [path("M 28 20 Q 50 8 72 20 V 76 Q 50 90 28 76 Z"),line(28,34,72,34,"SCORE"),line(28,62,72,62,"SCORE"),label(50,51,"LUNAR NEW YEAR",3,"middle")], "Lunar New Year", "review-recommended"),
        ("easter-egg", "Generic Easter egg starter", [path("M 50 7 C 75 15 86 55 72 80 C 62 96 38 96 28 80 C 14 55 25 15 50 7 Z"),path("M 25 50 Q 37 38 50 50 Q 63 62 75 50", "SCORE", False)], "Easter", "review-recommended"),
        ("halloween-pumpkin", "Generic Halloween pumpkin starter", [ellipse(50,55,38,32),rect(45,14,10,10,rx=2),path("M 32 52 L 40 42 L 46 53 Z","SCORE"),path("M 54 53 L 60 42 L 68 52 Z","SCORE"),path("M 35 66 Q 50 78 65 66","SCORE",False)], "Halloween", "none"),
        ("graduation-cap", "Generic school graduation-cap starter", [polygon([(10,40),(50,18),(90,40),(50,62)]),path("M 25 48 V 72 Q 50 88 75 72 V 48","SCORE",False),line(90,40,90,75,"SCORE")], "school celebrations", "none"),
        ("generic-flag", "Generic flag and team-sign blank", [rect(18,12,64,45),line(18,12,18,90,"CUT")], "countries and teams", "review-recommended"),
        ("map-research-plaque", "Map research plaque blank", [rect(8,15,84,70,rx=6),label(50,45,"MAP RESEARCH",5,"middle"),label(50,58,"VERIFY SOURCE + LICENCE",3,"middle")], "maps", "review-recommended"),
        ("canada-region-plaque", "Canadian province or territory research plaque", [rect(6,12,88,76,rx=6),label(50,42,"PROVINCE / TERRITORY",4,"middle"),label(50,56,"AUTHORITATIVE OUTLINE ONLY",2.8,"middle")], "Canada", "review-recommended"),
        ("sport-ball", "Generic sport ball starter", [circle(50,50,40),path("M 10 50 Q 50 20 90 50","SCORE",False),path("M 10 50 Q 50 80 90 50","SCORE",False)], "sports", "none"),
        ("jersey-number-blank", "Generic jersey-number sign blank", [path("M 18 22 L 35 10 H 65 L 82 22 L 72 42 L 65 36 V 92 H 35 V 36 L 28 42 Z"),label(50,68,"00",22,"middle")], "sports", "none"),
        ("animal-paw", "Generic animal paw starter", [circle(50,62,20),ellipse(27,36,9,13),ellipse(45,28,9,13),ellipse(63,30,9,13),ellipse(78,42,9,13)], "animals", "none"),
        ("animal-fish", "Generic fish starter", [ellipse(46,50,32,20),polygon([(72,50),(94,30),(94,70)]),circle(30,46,2)], "animals", "none"),
        ("nature-leaf", "Generic leaf starter", [path("M 12 78 C 18 25 55 10 88 12 C 82 48 55 82 12 78 Z"),path("M 16 74 Q 45 48 82 18","SCORE",False)], "nature", "none"),
        ("nature-mountain", "Generic mountain starter", [polygon([(8,85),(40,25),(55,50),(68,35),(92,85)]),path("M 31 42 L 40 25 L 49 41","SCORE",False)], "nature", "none"),
        ("transport-car", "Generic car starter", [path("M 10 62 L 20 42 H 72 L 88 58 V 75 H 10 Z"),circle(28,75,8),circle(72,75,8)], "transportation", "none"),
        ("transport-airplane", "Generic airplane starter", [path("M 50 6 L 60 42 L 90 58 V 68 L 58 60 L 58 84 L 70 92 H 30 L 42 84 L 42 60 L 10 68 V 58 L 40 42 Z")], "transportation", "none"),
        ("science-flask", "Generic science flask starter", [path("M 38 10 H 62 M 42 10 V 42 L 20 82 Q 18 90 28 90 H 72 Q 82 90 80 82 L 58 42 V 10", "CUT", False),line(30,68,70,68,"SCORE")], "science", "none"),
        ("technology-robot", "Generic technology robot starter", [rect(20,25,60,55,rx=6),circle(38,48,5),circle(62,48,5),line(35,65,65,65,"SCORE"),line(50,25,50,12,"CUT"),circle(50,10,3)], "technology", "none"),
        ("technology-circuit-board", "Generic circuit-board sign blank", [rect(10,10,80,80,rx=5),circle(20,20,2),circle(80,20,2),circle(20,80,2),circle(80,80,2),path("M 28 35 H 48 V 50 H 72 M 28 65 H 55 V 52","SCORE",False)], "technology", "none"),
        ("art-palette", "Generic art palette starter", [path("M 50 8 C 88 8 96 38 84 62 C 75 80 60 72 53 82 C 45 95 15 85 10 58 C 4 28 20 8 50 8 Z"),circle(30,35,5),circle(48,25,5),circle(67,33,5),circle(74,52,5)], "art", "none"),
        ("hobby-book", "Generic open-book starter", [path("M 8 22 Q 30 12 50 28 V 86 Q 30 70 8 78 Z"),path("M 92 22 Q 70 12 50 28 V 86 Q 70 70 92 78 Z")], "hobbies", "none"),
        ("occupation-hard-hat", "Generic hard-hat starter", [path("M 12 70 H 88 V 82 H 12 Z"),path("M 22 70 Q 22 25 50 18 Q 78 25 78 70", "CUT", False),line(50,18,50,64,"SCORE")], "occupations", "none"),
        ("architecture-house", "Generic house starter", [polygon([(10,45),(50,10),(90,45),(90,90),(10,90)]),rect(42,58,16,32),rect(20,52,14,14),rect(66,52,14,14)], "architecture", "none"),
        ("architecture-bridge", "Generic bridge starter", [path("M 5 78 H 95 V 88 H 5 Z"),path("M 14 78 Q 50 24 86 78", "CUT", False),line(50,32,50,78,"SCORE")], "architecture", "none"),
        ("sign-caution", "Generic caution sign blank", [polygon([(50,8),(94,88),(6,88)]),label(50,70,"!",36,"middle")], "signs and safety", "none"),
        ("sign-exit-arrow", "Generic directional arrow sign", [rect(6,18,88,64,rx=5),polygon([(25,50),(48,28),(48,42),(78,42),(78,58),(48,58),(48,72)]),label(20,72,"EXIT",5,"middle")], "signs and safety", "none"),
        ("ppe-label-board", "PPE label board starter", [rect(5,10,90,80,rx=5),circle(50,42,22),label(50,47,"PPE",10,"middle"),label(50,78,"LABEL REQUIRED EQUIPMENT",3,"middle")], "signs and safety", "none")
    ]
    for aid,title,geometry,sub,sensitivity in themes:
        operations=sorted({op for op in ("CUT","SCORE","ENGRAVE") if any(f'data-operation="{op}"' in g for g in geometry)})
        if not operations: operations=["CUT"]
        c.add(Asset(f"tc-theme-{aid}",title,"An original generic outline intended as a student design starting point, not a finished answer.",
            "themed-starters",sub,100,100,geometry,shop="general",tool_family="themed starter",tags=["theme",sub,aid],
            operations=operations,sensitivity=sensitivity,
            source_reference="Original procedural geometry. Review names and context before cultural or religious use.",
            notes="Generic starter only. Do not add sacred, restricted, branded or team imagery without authoritative sources and permission."))


def write_outputs(catalogue: Catalogue) -> None:
    if GENERATED.exists():
        shutil.rmtree(GENERATED)
    SVG_ROOT.mkdir(parents=True)
    PREVIEW_ROOT.mkdir(parents=True)
    manifest = []
    for asset in sorted(catalogue.assets, key=lambda value: value.id):
        metadata = catalogue.metadata(asset)
        manifest.append(metadata)
        svg_path = ROOT / metadata["files"]["svg"]
        preview_path = ROOT / metadata["files"]["preview"]
        svg_path.parent.mkdir(parents=True, exist_ok=True)
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        svg_path.write_text(svg_document(asset, metadata), encoding="utf-8", newline="\n")
        preview_path.write_text(svg_document(asset, metadata, preview=True), encoding="utf-8", newline="\n")

    summary: dict[str, int] = {}
    for record in manifest:
        summary[record["category"]] = summary.get(record["category"], 0) + 1
    document = {
        "schema_version": 1,
        "library": {key: catalogue.cfg[key] for key in ("id", "title", "version", "generator_version", "units", "license", "attribution", "source")},
        "generated_notice": "Deterministic output. Regenerate from laser/config and laser/scripts; do not hand-edit generated SVGs.",
        "physical_verification_notice": "All records remain unverified unless backed by a recorded physical test.",
        "count": len(manifest),
        "category_counts": dict(sorted(summary.items())),
        "assets": manifest,
    }
    catalog_path = GENERATED / "catalog.json"
    catalog_path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")

    columns = ["id","title","category","subcategory","shop","tool_family","technology_areas","skill_level","dimensions","operations","fit_type","svg","preview","license","sensitivity","trademark_status","review_status"]
    with (GENERATED / "catalog.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for item in manifest:
            writer.writerow({
                "id": item["id"], "title": item["title"], "category": item["category"], "subcategory": item["subcategory"],
                "shop": item["shop"], "tool_family": item["tool_family"],
                "technology_areas": "|".join(item["technology_areas"]), "skill_level": item["skill_level"],
                "dimensions": f'{item["dimensions"]["width"]} × {item["dimensions"]["height"]} mm',
                "operations": "+".join(item["operations"]), "fit_type": item["fit_type"], "svg": item["files"]["svg"],
                "preview": item["files"]["preview"], "license": item["license"], "sensitivity": item["sensitivity"],
                "trademark_status": item["trademark_status"], "review_status": item["review_status"],
            })

    files_for_hash = sorted(path for path in GENERATED.rglob("*") if path.is_file() and path.name != "SHA256SUMS")
    checksum_lines = []
    for file_path in files_for_hash:
        checksum_lines.append(f"{hashlib.sha256(file_path.read_bytes()).hexdigest()}  {file_path.relative_to(GENERATED).as_posix()}")
    (GENERATED / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8", newline="\n")

    bundle_path = GENERATED / "downloads" / "technology-commons-laser-library.zip"
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_files = [ROOT / "README.md", ROOT.parent / "LICENSE.md", ROOT / "docs" / "PHYSICAL-TEST-BATCH.md", catalog_path, GENERATED / "catalog.csv"]
    bundle_files += sorted(SVG_ROOT.rglob("*.svg"))
    with zipfile.ZipFile(bundle_path, "w", compression=zipfile.ZIP_STORED) as archive:
        for file_path in bundle_files:
            if file_path.is_relative_to(GENERATED):
                arcname = Path("technology-commons-laser-library") / file_path.relative_to(GENERATED)
            elif file_path.is_relative_to(ROOT):
                arcname = Path("technology-commons-laser-library") / file_path.relative_to(ROOT)
            else:
                arcname = Path("technology-commons-laser-library") / file_path.name
            info = zipfile.ZipInfo(arcname.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.compress_type = zipfile.ZIP_STORED
            info.external_attr = 0o100644 << 16
            payload = file_path.read_bytes()
            if file_path.suffix.lower() in {".csv", ".json", ".md", ".svg", ".txt", ".yml", ".yaml"}:
                payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            archive.writestr(info, payload)
    print(f"Generated {len(manifest)} assets across {len(summary)} categories")
    print(f"Manifest: {catalog_path.relative_to(ROOT)}")
    print(f"Bundle: {bundle_path.relative_to(ROOT)}")


def build_catalogue(config: dict[str, Any]) -> Catalogue:
    catalogue = Catalogue(config)
    add_calibration(catalogue)
    add_size_families(catalogue)
    add_core_geometry(catalogue)
    add_french_cleat(catalogue)
    add_holders(catalogue)
    add_jigs_gauges(catalogue)
    add_jigs_projects_themes(catalogue)
    return catalogue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="regenerate in place and report catalogue count")
    parser.parse_args()
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    write_outputs(build_catalogue(config))
    generate_classroom_kit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
