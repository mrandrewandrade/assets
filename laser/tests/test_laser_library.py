"""Regression tests for the Technology Commons laser library."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "generated" / "catalog.json"
SVG = "{http://www.w3.org/2000/svg}"


class LaserLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.run([sys.executable, str(ROOT / "scripts" / "generate_library.py")], check=True, cwd=ROOT.parent)
        cls.document = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.assets = {item["id"]: item for item in cls.document["assets"]}

    def test_catalogue_is_substantial_and_ids_unique(self) -> None:
        self.assertGreaterEqual(len(self.assets), 150)
        self.assertEqual(len(self.assets), self.document["count"])

    def test_50_mm_circle_is_really_50_mm(self) -> None:
        record = self.assets["tc-disc-50mm"]
        root = ET.parse(ROOT / record["files"]["svg"]).getroot()
        circles = root.findall(f".//{SVG}circle")
        self.assertTrue(any(abs(float(node.attrib["r"]) * 2 - 50) < 1e-9 for node in circles))
        self.assertEqual(record["dimensional_tests"]["circle_diameter_mm"], 50)

    def test_100_by_200_plate_is_really_100_by_200_mm(self) -> None:
        record = self.assets["tc-rectangle-100x200mm"]
        root = ET.parse(ROOT / record["files"]["svg"]).getroot()
        outer = root.find(f".//{SVG}rect")
        self.assertIsNotNone(outer)
        self.assertEqual(float(outer.attrib["width"]), 100)
        self.assertEqual(float(outer.attrib["height"]), 200)
        self.assertEqual(root.attrib["width"], "100mm")
        self.assertEqual(root.attrib["height"], "200mm")
        self.assertEqual(root.attrib["viewBox"], "0 0 100 200")

    def test_fit_assets_record_measured_thickness(self) -> None:
        record = self.assets["tc-cal-slot-fit"]
        self.assertEqual(record["parameters"]["material_thickness_mm"], 6.0)
        self.assertIn("Measure every sheet", record["material"]["warning"])
        self.assertEqual(record["review_status"], "unverified")

    def test_screw_length_gauge_is_a_linear_length_scale(self) -> None:
        record = self.assets["tc-jig-screw-length"]
        root = ET.parse(ROOT / record["files"]["svg"]).getroot()
        self.assertEqual(record["parameters"]["measurement_axis"], "under-head-to-tip")
        self.assertEqual(record["dimensional_tests"]["scale_length_mm"], 120)
        self.assertEqual(root.findall(f".//{SVG}circle"), [])
        self.assertGreaterEqual(len(root.findall(f".//{SVG}line")), 120)

    def test_jigs_have_specific_geometry_and_metadata(self) -> None:
        jigs = [record for record in self.document["assets"] if record["category"] == "jigs-gauges"]
        self.assertGreaterEqual(len(jigs), 15)
        for record in jigs:
            self.assertNotIn("starter template", record["description"].lower())
            self.assertTrue(record["parameters"], record["id"])
            self.assertTrue(record["dimensional_tests"], record["id"])
        self.assertEqual(self.assets["tc-jig-pcb-spacing"]["parameters"]["pitch_mm"], 2.54)

    def test_unreviewed_shop_taxonomy_is_not_published_as_fake_holders(self) -> None:
        self.assertFalse(any(asset_id.startswith("tc-organizer-") for asset_id in self.assets))

    def test_technology_area_tags_are_selective_and_complete(self) -> None:
        expected = {
            "exploring-technologies", "technological-design", "manufacturing", "construction",
            "transportation", "computer-technology", "communications-technology", "green-industries",
            "hairstyling-aesthetics", "hospitality-tourism", "health-care",
        }
        represented = {area for record in self.assets.values() for area in record["technology_areas"]}
        self.assertEqual(represented, expected)
        self.assertTrue(all(1 <= len(record["technology_areas"]) <= 6 for record in self.assets.values()))
        self.assertIn("transportation", self.assets["tc-holder-socket-rack"]["technology_areas"])
        self.assertIn("computer-technology", self.assets["tc-jig-pcb-spacing"]["technology_areas"])
        self.assertIn("green-industries", self.assets["tc-theme-nature-leaf"]["technology_areas"])
        self.assertIn("hospitality-tourism", self.assets["tc-project-coaster-blank"]["technology_areas"])
        self.assertNotIn("health-care", self.assets["tc-holder-socket-rack"]["technology_areas"])

    def test_published_holders_are_multi_part_rack_kits(self) -> None:
        holders = [record for record in self.document["assets"] if record["category"] == "tool-holders"]
        self.assertEqual(len(holders), 18)
        for record in holders:
            self.assertEqual(len(record["parameters"]["components"]), 5, record["id"])
            root = ET.parse(ROOT / record["files"]["svg"]).getroot()
            self.assertGreaterEqual(len(root.findall(f".//{SVG}rect")), 3, record["id"])
            self.assertEqual(len(root.findall(f".//{SVG}polygon")), 2, record["id"])

    def test_all_fabrication_svgs_have_mm_canvas_and_no_raster(self) -> None:
        for record in self.document["assets"]:
            path = ROOT / record["files"]["svg"]
            raw = path.read_text(encoding="utf-8").lower()
            root = ET.fromstring(raw)
            self.assertTrue(root.attrib["width"].endswith("mm"), path)
            self.assertTrue(root.attrib["height"].endswith("mm"), path)
            self.assertNotIn("<image", raw, path)
            self.assertNotIn(" transform=", raw, path)

    def test_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_library.py"), "--json"],
            cwd=ROOT.parent, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
