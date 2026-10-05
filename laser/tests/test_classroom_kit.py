"""Regression tests for the focused first-project classroom kit."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "generated" / "classroom-kit"
SVG = "{http://www.w3.org/2000/svg}"


class ClassroomKitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_classroom_kit.py")], check=True, cwd=ROOT.parent)

    def test_six_named_palettes_are_true_size_svg(self) -> None:
        expected = {"basic-geometry", "hole", "slot", "structure", "wall-mounting", "organizer"}
        found = {path.stem for path in (KIT / "palettes").glob("*.svg")}
        self.assertEqual(found, expected)
        for path in (KIT / "palettes").glob("*.svg"):
            root = ET.parse(path).getroot()
            self.assertTrue(root.attrib["width"].endswith("mm"))
            self.assertTrue(root.attrib["height"].endswith("mm"))
            self.assertEqual(root.attrib["viewBox"], "0 0 216 170")
            raw = path.read_text(encoding="utf-8").lower()
            self.assertNotIn(" display=\"none\"", raw)
            self.assertNotIn("<image", raw)
            self.assertNotIn(" transform=", raw)

    def test_hole_palette_teaches_semantic_difference(self) -> None:
        root = ET.parse(KIT / "palettes" / "hole.svg").getroot()
        hole = root.find(f".//{SVG}g[@id='component-bottle-opening-36']")
        disc = root.find(f".//{SVG}g[@id='component-disc-36']")
        self.assertEqual(hole.attrib["data-semantic"], "hole")
        self.assertEqual(disc.attrib["data-semantic"], "circle-part")

    def test_five_pill_bottle_references_have_bom_and_status(self) -> None:
        document = json.loads((KIT / "pill-bottle" / "assemblies.json").read_text(encoding="utf-8"))
        self.assertEqual(len(document["designs"]), 5)
        for design in document["designs"].values():
            self.assertGreaterEqual(len(design["bom"]), 3)
            self.assertEqual(design["physical_test_status"], "unverified")
            self.assertEqual(design["parameters"]["opening_diameter_mm"], 36.0)
            for relative in design["files"].values():
                self.assertTrue((KIT / relative).is_file())

        captured = document["designs"]["captured-bottle-rack"]
        self.assertEqual(captured["parameters"]["keeper_opening_diameter_mm"], 38.0)
        self.assertGreaterEqual(len(captured["parameters"]["service_sequence"]), 5)
        self.assertGreaterEqual(len(captured["parameters"]["physical_test_record_fields"]), 6)
        self.assertGreaterEqual(len(captured["bom"]), 6)

    def test_organizer_palette_includes_serviceable_keeper_parts(self) -> None:
        root = ET.parse(KIT / "palettes" / "organizer.svg").getroot()
        self.assertIsNotNone(root.find(f".//{SVG}g[@id='component-keeper-rail']"))
        self.assertIsNotNone(root.find(f".//{SVG}g[@id='component-keeper-plate']"))

    def test_name_tag_and_stand_assets_exist(self) -> None:
        self.assertTrue((KIT / "name-tag" / "name-tag-engraving-template.svg").is_file())
        self.assertTrue((KIT / "name-tag" / "name-tag-layout-examples.svg").is_file())
        self.assertTrue((KIT / "standing-name-tag" / "standing-name-tag-components.svg").is_file())

    def test_individual_components_are_label_free_and_exact_size(self) -> None:
        components = list((KIT / "components").glob("*.svg"))
        self.assertGreaterEqual(len(components), 8)
        for path in components:
            root = ET.parse(path).getroot()
            self.assertTrue(root.attrib["width"].endswith("mm"))
            self.assertTrue(root.attrib["height"].endswith("mm"))
            self.assertEqual(root.findall(f".//{SVG}text"), [], path)
            self.assertNotIn(" transform=", path.read_text(encoding="utf-8").lower())

    def test_bundle_and_manifest_exist(self) -> None:
        manifest = json.loads((KIT / "manifest.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(manifest["files"]), 26)
        self.assertTrue((KIT / "technology-commons-first-laser-projects.zip").stat().st_size > 0)

    def test_bundle_is_cross_platform_deterministic(self) -> None:
        archive_path = KIT / "technology-commons-first-laser-projects.zip"
        text_suffixes = {".csv", ".json", ".md", ".svg", ".txt", ".yml", ".yaml"}
        with zipfile.ZipFile(archive_path) as archive:
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            for info in archive.infolist():
                self.assertEqual(info.compress_type, zipfile.ZIP_STORED)
                self.assertEqual(info.date_time, (2026, 1, 1, 0, 0, 0))
                if Path(info.filename).suffix.lower() in text_suffixes or Path(info.filename).name == "SHA256SUMS":
                    self.assertNotIn(b"\r", archive.read(info))


if __name__ == "__main__":
    unittest.main()
