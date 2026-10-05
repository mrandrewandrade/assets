#!/usr/bin/env python3
"""Generate the focused Technology Commons laser classroom kit.

The kit is intentionally separate from the large browseable catalogue.  It
contains a small number of reusable component palettes, project templates and
worked reference assemblies for the first active classroom sequence.

SPDX-License-Identifier: CC-BY-SA-4.0
"""

from __future__ import annotations

import hashlib
import html
import json
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "classroom-kit"
VERSION = "1.0.0"

CUT = '#ff0000'
SCORE = '#0000ff'
ENGRAVE = '#111111'
GUIDE = '#7b8794'


def n(value: float) -> str:
    return f"{value:.4f}".rstrip("0").rstrip(".") or "0"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def line(x1: float, y1: float, x2: float, y2: float, role: str = "SCORE") -> str:
    colour = SCORE if role == "SCORE" else ENGRAVE
    return f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" fill="none" stroke="{colour}" stroke-width="0.25" vector-effect="non-scaling-stroke" data-operation="{role}"/>'


def rect(x: float, y: float, w: float, h: float, role: str = "CUT", rx: float = 0, *, colour: str | None = None, dash: str | None = None) -> str:
    stroke = colour or (CUT if role == "CUT" else SCORE if role == "SCORE" else ENGRAVE)
    rounded = f' rx="{n(rx)}" ry="{n(rx)}"' if rx else ""
    dashed = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{rounded} fill="none" stroke="{stroke}" stroke-width="0.25" vector-effect="non-scaling-stroke"{dashed} data-operation="{role}"/>'


def circle(cx: float, cy: float, diameter: float, role: str = "CUT", *, colour: str | None = None) -> str:
    stroke = colour or (CUT if role == "CUT" else SCORE if role == "SCORE" else ENGRAVE)
    return f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(diameter / 2)}" fill="none" stroke="{stroke}" stroke-width="0.25" vector-effect="non-scaling-stroke" data-operation="{role}"/>'


def polygon(points: Iterable[tuple[float, float]], role: str = "CUT") -> str:
    value = " ".join(f"{n(x)},{n(y)}" for x, y in points)
    return f'<polygon points="{value}" fill="none" stroke="{CUT}" stroke-width="0.25" vector-effect="non-scaling-stroke" data-operation="{role}"/>'


def path(d: str, role: str = "CUT") -> str:
    colour = CUT if role == "CUT" else SCORE if role == "SCORE" else ENGRAVE
    return f'<path d="{d}" fill="none" stroke="{colour}" stroke-width="0.25" vector-effect="non-scaling-stroke" data-operation="{role}"/>'


def text(x: float, y: float, value: str, size: float = 4, anchor: str = "start", weight: int = 400, colour: str = ENGRAVE) -> str:
    return f'<text x="{n(x)}" y="{n(y)}" fill="{colour}" stroke="none" font-family="Arial, sans-serif" font-size="{n(size)}" font-weight="{weight}" text-anchor="{anchor}" data-role="annotation">{esc(value)}</text>'


def group(identifier: str, label: str, geometry: Iterable[str], **metadata: object) -> str:
    attrs = " ".join(f'data-{key.replace("_", "-")}="{esc(str(value))}"' for key, value in metadata.items())
    return f'<g id="{esc(identifier)}" aria-label="{esc(label)}" {attrs}>\n' + "\n".join(geometry) + "\n</g>"


def svg(title: str, description: str, width: float, height: float, body: Iterable[str], metadata: dict[str, object]) -> str:
    meta = {"title": title, "description": description, "units": "mm", "version": VERSION, "review_status": "unverified", **metadata}
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{n(width)}mm" height="{n(height)}mm" viewBox="0 0 {n(width)} {n(height)}">\n'
        f'<title>{esc(title)}</title>\n<desc>{esc(description)}</desc>\n'
        f'<metadata id="technology-commons-classroom-kit">{esc(json.dumps(meta, sort_keys=True, separators=(",", ":")))}</metadata>\n'
        + "\n".join(body)
        + "\n</svg>\n"
    )


@dataclass(frozen=True)
class GeneratedFile:
    path: str
    title: str
    kind: str
    description: str
    parameters: dict[str, object]
    review_status: str = "unverified"


def write(relative: str, content: str) -> None:
    target = OUT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def palette_header(title: str, subtitle: str) -> list[str]:
    return [text(10, 12, title, 7, weight=700), text(10, 20, subtitle, 3.6, colour=GUIDE),
            text(10, 27, "RED = CUT · BLUE = SCORE · dimensions in mm · test before production", 3.2, colour=GUIDE)]


def palette_card(x: float, y: float, w: float, h: float, identifier: str, title: str, note: str, geometry: Iterable[str], **meta: object) -> str:
    return group(identifier, title, [rect(x, y, w, h, "ENGRAVE", colour="#c5cbd3", rx=2, dash="2 2"), text(x + 5, y + 8, title, 4.3, weight=700), text(x + 5, y + h - 5, note, 3.2, colour=GUIDE), *geometry], **meta)


def generate_palettes() -> list[GeneratedFile]:
    files: list[GeneratedFile] = []
    palettes: list[tuple[str, str, str, list[str], dict[str, object]]] = []

    body = palette_header("BASIC GEOMETRY", "Copy a named group; set exact W/H in Inkscape before arranging the project.")
    body += [
        palette_card(8, 34, 96, 60, "component-rectangle-60x30", "Rectangle part", "60 × 30", [rect(26, 51, 60, 30)], width_mm=60, height_mm=30),
        palette_card(112, 34, 96, 60, "component-rounded-60x30", "Rounded rectangle", "60 × 30 · R5", [rect(130, 51, 60, 30, rx=5)], width_mm=60, height_mm=30, radius_mm=5),
        palette_card(8, 102, 96, 60, "component-disc-40", "Circle part", "Ø40 · material kept", [circle(56, 128, 40)], diameter_mm=40, semantic="circle-part"),
        palette_card(112, 102, 96, 60, "component-triangle-50", "Triangle part", "50 base × 40 high", [polygon([(135,145),(185,145),(160,105)])], base_mm=50, height_mm=40),
    ]
    palettes.append(("palettes/basic-geometry.svg", "Basic Geometry Palette", "Exact-size primitive parts for Inkscape.", body, {"palette": "basic-geometry"}))

    body = palette_header("HOLES + CIRCLE PARTS", "A hole removes material inside a larger part. A circle part keeps the disc.")
    body += [
        palette_card(8, 34, 96, 60, "component-hole-6", "Ø6 hole in coupon", "HOLE · removes centre", [rect(25,49,62,32), circle(56,65,6)], diameter_mm=6, semantic="hole"),
        palette_card(112, 34, 96, 60, "component-hole-10", "Ø10 hole in coupon", "HOLE · verify hardware", [rect(129,49,62,32), circle(160,65,10)], diameter_mm=10, semantic="hole"),
        palette_card(8, 102, 96, 60, "component-bottle-opening-36", "Ø36 bottle opening", "HOLE · 34 body + clearance", [rect(23,112,66,40), circle(56,132,36)], diameter_mm=36, semantic="hole"),
        palette_card(112, 102, 96, 60, "component-disc-36", "Ø36 circle part", "DISC · opposite cut result", [circle(160,132,36)], diameter_mm=36, semantic="circle-part"),
    ]
    palettes.append(("palettes/hole.svg", "Hole Palette", "Hole and circle-part semantics shown with exact geometry.", body, {"palette": "hole", "kerf_note": "Nominal geometry is not finished fit; cut a test coupon."}))

    body = palette_header("SLOTS", "Slot width begins with measured material thickness, then changes after a physical fit test.")
    for i, (name, width, note) in enumerate((("press", 5.85, "start −0.15"), ("snug", 6.0, "start nominal"), ("slip", 6.15, "start +0.15"), ("loose", 6.3, "start +0.30"))):
        x = 8 + (i % 2) * 104
        y = 34 + (i // 2) * 68
        body.append(palette_card(x, y, 96, 60, f"component-slot-{name}", f"{name.title()} slot", f"{width:.2f} wide · {note}", [path(f"M {n(x+34)} {n(y+16)} V {n(y+49)} H {n(x+34+width)} V {n(y+16)}")], slot_width_mm=width, material_example_mm=6.0, fit=name))
    palettes.append(("palettes/slot.svg", "Slot Palette", "Four fit starting points for measured 6 mm material.", body, {"palette": "slot", "material_example_mm": 6.0}))

    body = palette_header("STRUCTURE", "Parts support a load only after material, grain, joints and assembly have been tested.")
    body += [
        palette_card(8,34,96,60,"component-gusset-50","Triangular gusset","50 × 50",[polygon([(30,82),(80,82),(30,32)])], width_mm=50,height_mm=50),
        palette_card(112,34,96,60,"component-t-foot","T-foot","80 × 35 · slot 6",[path("M 124 79 H 204 V 89 H 168 V 64 H 160 V 89 H 124 Z")], width_mm=80,height_mm=35,slot_width_mm=8),
        palette_card(8,102,96,60,"component-brace-80","Brace rail","80 × 16",[rect(16,122,80,16)],width_mm=80,height_mm=16),
        palette_card(112,102,96,60,"component-easel-leg","Easel leg","70 × 18 · pivot Ø4",[rect(125,121,70,18,rx=4),circle(187,130,4)],width_mm=70,height_mm=18,pivot_mm=4),
    ]
    palettes.append(("palettes/structure.svg", "Structure Palette", "Reusable supports, feet and braces.", body, {"palette": "structure"}))

    body = palette_header("WALL + MOUNTING", "The wall, fasteners and anchors carry the load. Laser-cut parts are not automatically load-rated.")
    body += [
        palette_card(8,34,96,60,"component-two-hole-mount","Two-hole mount","100 × 30 · Ø5",[rect(15,51,82,25,rx=3),circle(28,63.5,5),circle(84,63.5,5)],hole_mm=5,spacing_mm=56),
        palette_card(112,34,96,60,"component-keyhole-plate","Keyhole test plate","80 × 32 · test screw head",[rect(120,50,80,32,rx=3),circle(135,62,10),path("M 132 64 H 138 V 76 H 132 Z")],review="prototype-only"),
        palette_card(8,102,96,60,"component-cleat-face","Cleat module face","90 × 40",[rect(11,115,90,40),line(18,143,94,143,"SCORE")],width_mm=90,height_mm=40),
        palette_card(112,102,96,60,"component-removable-foot","Bench foot","70 × 28 · slot 6",[path("M 125 124 H 195 V 152 H 169 V 138 H 163 V 152 H 125 Z")],width_mm=70,height_mm=28,slot_width_mm=6),
    ]
    palettes.append(("palettes/wall-mounting.svg", "Wall and Mounting Palette", "Mounting and removable-module building blocks.", body, {"palette": "wall-mounting", "safety": "Instructor approval and load testing required."}))

    body = palette_header("ORGANIZER", "Measure the object, choose the controlling diameter, then add retention only when the use needs it.")
    body += [
        palette_card(8,34,96,60,"component-bottle-retainer","Bottle retainer","Ø36 opening · Ø54 ring",[circle(56,64,54),circle(56,64,36)],opening_mm=36,outer_mm=54),
        palette_card(112,34,96,60,"component-four-opening-row","Four-opening row","Ø36 · 42 centres",[rect(118,48,84,32),*[circle(128+i*21,64,18) for i in range(4)]],opening_mm=18,spacing_mm=21,usage_note="Half-scale study; scale dimensions numerically."),
        palette_card(8,102,96,60,"component-label-tab","Label tab","60 × 18 · R3",[rect(26,123,60,18,rx=3)],width_mm=60,height_mm=18),
        palette_card(112,102,46,60,"component-divider","Divider","32 × 35 · slot",[path("M 119 118 H 151 V 153 H 137 V 140 H 131 V 153 H 119 Z")],width_mm=32,height_mm=35,slot_width_mm=6),
        palette_card(162,102,46,27,"component-keeper-rail","Keeper rail","42 × 12",[rect(164,114,42,12,rx=2)],width_mm=42,height_mm=12,semantic="removable-retention"),
        palette_card(162,135,46,27,"component-keeper-plate","Keeper plate","Ø38 opening",[rect(164,143,42,16,rx=2),circle(185,151,12)],opening_mm=12,usage_note="Scale from measured body/cap; keep removable."),
    ]
    palettes.append(("palettes/organizer.svg", "Organizer Palette", "Measured openings, labels and dividers.", body, {"palette": "organizer"}))

    for relative, title, description, body, metadata in palettes:
        write(relative, svg(title, description, 216, 170, body, metadata))
        files.append(GeneratedFile(relative, title, "palette", description, metadata))
    return files


def generate_individual_components() -> list[GeneratedFile]:
    """Write clean, label-free parts that can be imported directly at 100%."""
    specs = [
        ("rectangle-60x30", "Rectangle Part 60 × 30", 60, 30, [rect(0,0,60,30)], {"width_mm":60,"height_mm":30,"semantic":"part"}),
        ("circle-part-40", "Circle Part Ø40", 40, 40, [circle(20,20,40)], {"diameter_mm":40,"semantic":"circle-part"}),
        ("hole-coupon-6", "Hole Coupon Ø6", 60, 30, [rect(0,0,60,30),circle(30,15,6)], {"diameter_mm":6,"semantic":"hole"}),
        ("slot-coupon-6p15", "Slip Slot Coupon 6.15", 50, 35, [path("M 20 0 V 28 H 26.15 V 0"),rect(0.25,0.25,49.5,34.5)], {"slot_width_mm":6.15,"material_example_mm":6.0,"fit":"slip"}),
        ("gusset-50", "Right-Triangle Gusset 50", 50, 50, [polygon([(0,50),(50,50),(0,0)])], {"width_mm":50,"height_mm":50,"semantic":"structure"}),
        ("two-hole-mount-100x30", "Two-Hole Mount Plate", 100, 30, [rect(0,0,100,30,rx=3),circle(15,15,5),circle(85,15,5)], {"hole_mm":5,"spacing_mm":70,"semantic":"mounting"}),
        ("bottle-retainer-36", "Bottle Retainer Ring", 54, 54, [circle(27,27,54),circle(27,27,36)], {"opening_mm":36,"outer_mm":54,"semantic":"organizer"}),
        ("label-tab-60x18", "Label Tab", 60, 18, [rect(0,0,60,18,rx=3)], {"width_mm":60,"height_mm":18,"semantic":"organizer"}),
    ]
    files: list[GeneratedFile] = []
    for identifier, title, width, height, geometry, parameters in specs:
        relative = f"components/{identifier}.svg"
        write(relative, svg(title, "Label-free exact-size component for import into an Inkscape project.", width, height, [group(f"component-{identifier}", title, geometry, **parameters)], {"component":identifier,"parameters":parameters,"physical_test_status":"unverified"}))
        files.append(GeneratedFile(relative,title,"individual-component","Exact-size label-free component.",parameters))
    return files


def generate_name_tag() -> list[GeneratedFile]:
    files: list[GeneratedFile] = []
    template_body = [
        text(8, 9, "NAME + LOGO ENGRAVING TEMPLATE", 5.5, weight=700),
        text(8, 16, "Set page to the measured blank size before exporting PNG.", 3.2, colour=GUIDE),
        group("blank-boundary-guide", "Measured blank boundary (guide only)", [rect(10,24,100,40,"ENGRAVE",colour=GUIDE,dash="2 2")], output="guide-only", default_width_mm=100, default_height_mm=40),
        group("safe-area-guide", "Safe area (guide only)", [rect(15,29,90,30,"ENGRAVE",colour="#9aa3ad",dash="1 1")], output="guide-only", default_margin_mm=5),
        group("student-name-placeholder", "Replace with student name", [text(60,44,"YOUR NAME",9,"middle",700)], output="engrave"),
        group("student-logo-placeholder", "Replace with original logo", [circle(94,44,14,"ENGRAVE"), text(94,46,"A",7,"middle",700)], output="engrave"),
        text(10, 72, "Delete both guides before export · crop to page · export at instructor-set DPI", 3.2, colour=GUIDE),
    ]
    relative = "name-tag/name-tag-engraving-template.svg"
    write(relative, svg("Name and Logo Engraving Template", "Editable Inkscape source for a measured, pre-cut rectangular blank.", 120, 80, template_body, {"project": "name-logo", "output": "PNG engraving artwork", "default_blank_mm": [100,40], "safe_margin_mm": 5}))
    files.append(GeneratedFile(relative, "Name and Logo Engraving Template", "project-template", "Editable template for a measured pre-cut blank.", {"default_blank_mm": [100,40], "safe_margin_mm": 5}))

    examples = [text(8,9,"NAME + LOGO LAYOUT CHECK",5.5,weight=700), text(8,16,"Three workable arrangements and three problems to fix before export.",3.2,colour=GUIDE)]
    cards = [
        (8,23,"GOOD · balanced","MAYA","M",True), (82,23,"GOOD · left mark","NOAH","N",True), (156,23,"GOOD · stacked","LI","L",True),
        (8,75,"FIX · clipped","ALEXANDRA","A",False), (82,75,"FIX · tiny name","SAM","S",False), (156,75,"FIX · weak contrast","RILEY","R",False),
    ]
    for x,y,label_value,name_value,mark,good in cards:
        examples += [text(x,y,label_value,3.3,weight=700,colour="#176f4d" if good else "#a33b2b"),rect(x,y+5,64,34,"ENGRAVE",colour=GUIDE,rx=2)]
        size = 7 if good else (7 if "clipped" in label_value else 3)
        name_x = x+32 if "stacked" in label_value else x+8
        anchor = "middle" if "stacked" in label_value else "start"
        examples.append(text(name_x,y+25,name_value,size,anchor,700,colour=ENGRAVE if good or "weak" not in label_value else "#b9bec4"))
        examples.append(circle(x+54,y+22,12,"ENGRAVE",colour=ENGRAVE if good else "#b9bec4"))
        examples.append(text(x+54,y+24,mark,5,"middle",700,colour=ENGRAVE if good else "#b9bec4"))
    relative = "name-tag/name-tag-layout-examples.svg"
    write(relative, svg("Name and Logo Layout Examples", "Three workable layout patterns and three common problems.", 228, 120, examples, {"project": "name-logo", "purpose": "layout critique"}))
    files.append(GeneratedFile(relative, "Name and Logo Layout Examples", "teacher-diagram", "Good and poor engraving layouts for critique.", {}))
    return files


def part_label(x: float, y: float, name_value: str, quantity: int, dimensions: str) -> list[str]:
    return [text(x,y,name_value,3.6,weight=700), text(x,y+5,f"QTY {quantity} · {dimensions}",2.8,colour=GUIDE)]


def bottle_holes(start_x: float, y: float, count: int = 4, spacing: float = 42, opening: float = 36) -> list[str]:
    return [circle(start_x + index * spacing, y, opening) for index in range(count)]


def example_sheet(kind: str) -> tuple[str, dict[str, object], list[dict[str, object]]]:
    opening, centres, count = 36.0, 42.0, 4
    params: dict[str, object] = {
        "bottle_body_diameter_mm": 34.0,
        "cap_diameter_mm": 42.0,
        "radial_clearance_mm": 1.0,
        "opening_diameter_mm": opening,
        "centre_spacing_mm": centres,
        "capacity": count,
        "material_thickness_example_mm": 6.0,
        "physical_test_status": "unverified",
    }
    g: list[str] = [text(8,10,kind.replace("-"," ").upper(),6,weight=700), text(8,17,"Reference assembly · verify bottle, material, kerf, joints and mounting",3.1,colour=GUIDE)]
    bom: list[dict[str, object]] = []
    if kind == "simple-shelf-rack":
        g += part_label(8,29,"TOP SHELF",1,"190 × 70 · 4 × Ø36")
        g += [rect(8,34,190,70,rx=3), *bottle_holes(38,69,count,centres,opening),rect(18,86,20,6.2),rect(168,86,20,6.2)]
        g += part_label(8,119,"BASE",1,"190 × 55 · 2 slots") + [rect(8,124,190,55,rx=3),rect(18,143,20,6.2),rect(168,143,20,6.2)]
        side_path_1 = "M 218 40 H 235 V 34 H 255 V 40 H 273 V 118 H 255 V 124 H 235 V 118 H 218 Z"
        side_path_2 = "M 283 40 H 300 V 34 H 320 V 40 H 338 V 118 H 320 V 124 H 300 V 118 H 283 Z"
        g += part_label(218,29,"SIDE",2,"55 × 90 · 20 × 6 tabs") + [path(side_path_1), path(side_path_2)]
        bom = [{"part":"top shelf","qty":1,"size_mm":[190,70]},{"part":"base","qty":1,"size_mm":[190,55]},{"part":"side","qty":2,"size_mm":[55,90]}]
        params.update({"slot_start_mm":6.2,"tab_width_mm":20,"assembly":"side tabs locate in matching shelf and base slots; dry-fit before adhesive or approved fasteners", "mounting":"bench/free-standing"})
    elif kind == "dowel-supported-rack":
        for y,title_value in ((34,"TOP PLATE"),(124,"BOTTOM PLATE")):
            g += part_label(8,y-5,title_value,1,"190 × 70 · 4 × Ø36 · 4 × Ø6.4")
            g += [rect(8,y,190,70,rx=3), *bottle_holes(38,y+35,count,centres,opening)]
            g += [circle(18,y+10,6.4),circle(188,y+10,6.4),circle(18,y+60,6.4),circle(188,y+60,6.4)]
        g += part_label(218,29,"DOWEL",4,"Ø6 × 85 long (purchased)")
        g += [circle(234+i*25,55,6,"ENGRAVE") for i in range(4)]
        bom = [{"part":"top plate","qty":1,"size_mm":[190,70]},{"part":"bottom plate","qty":1,"size_mm":[190,70]},{"part":"6 mm dowel","qty":4,"length_mm":85}]
        params.update({"dowel_diameter_mm":6.0,"dowel_hole_start_mm":6.4,"assembly":"dowels align and separate two plates","mounting":"bench/free-standing"})
    elif kind == "reinforced-wall-rack":
        shelf_path = "M 8 34 H 78 V 28 H 108 V 34 H 198 V 104 H 108 V 110 H 78 V 104 H 8 Z"
        g += part_label(8,29,"SHELF",1,"190 × 70 · tabs + 4 × Ø36") + [path(shelf_path),*bottle_holes(38,69,count,centres,opening)]
        g += part_label(8,119,"BACK",1,"190 × 90 · slots + 3 × Ø5 mount") + [rect(8,124,190,90,rx=3),circle(28,143,5),circle(103,143,5),circle(178,143,5),rect(78,168,30,6.2),rect(128,168,30,6.2)]
        g += part_label(218,29,"GUSSET",2,"60 × 60") + [polygon([(218,94),(278,94),(218,34)]),polygon([(288,94),(348,94),(288,34)])]
        bom = [{"part":"shelf","qty":1,"size_mm":[190,70]},{"part":"back","qty":1,"size_mm":[190,90]},{"part":"gusset","qty":2,"size_mm":[60,60]},{"part":"approved wall fastener","qty":3,"size":"site-specific"}]
        params.update({"slot_start_mm":6.2,"shelf_tab_width_mm":30,"assembly":"two shelf tabs locate in the back; gussets reinforce the shelf-to-back joint","mounting":"wall","safety":"Instructor approves wall, anchors, fasteners and load test."})
    elif kind == "removable-wall-bench-rack":
        g += part_label(8,29,"REMOVABLE SHELF",1,"190 × 70 · 4 × Ø36") + [rect(8,34,190,70,rx=3),*bottle_holes(38,69,count,centres,opening)]
        g += part_label(8,119,"MODULE BACK",1,"190 × 70 · 2 × Ø6.4 interface") + [rect(8,124,190,70,rx=3),circle(38,159,6.4),circle(168,159,6.4),line(18,180,188,180,"SCORE")]
        g += part_label(218,29,"BENCH FOOT",2,"70 × 28 · Ø6.4 + slot") + [path("M 218 54 H 288 V 82 H 262 V 68 H 256 V 82 H 218 Z"),circle(278,64,6.4),path("M 298 54 H 368 V 82 H 342 V 68 H 336 V 82 H 298 Z"),circle(308,64,6.4)]
        g += part_label(218,103,"WALL ADAPTER",1,"170 × 45 · 2 × Ø6.4 + mounts") + [rect(218,108,170,45,rx=3),circle(238,130,5),circle(368,130,5),circle(238,143,6.4),circle(368,143,6.4)]
        bom = [{"part":"shelf","qty":1,"size_mm":[190,70]},{"part":"module back","qty":1,"size_mm":[190,70]},{"part":"bench foot","qty":2,"size_mm":[70,28]},{"part":"wall adapter","qty":1,"size_mm":[170,45]},{"part":"M6 hand knob, bolt and washer set","qty":2,"size":"site-specific"}]
        params.update({"interface_hole_mm":6.4,"interface_spacing_mm":130,"assembly":"two removable M6 hand knobs register the same module to either bench supports or an approved wall adapter","mounting":"removable wall/bench","safety":"Adapter interface and wall installation require instructor approval and load testing."})
    else:
        g += part_label(8,29,"LOWER LOCATING PLATE",1,"190 × 70 · 4 × Ø36") + [rect(8,34,190,70,rx=3),*bottle_holes(38,69,count,centres,opening)]
        g += part_label(8,119,"BASE",1,"190 × 55") + [rect(8,124,190,55,rx=3)]
        g += part_label(208,29,"UPPER KEEPER PLATE",1,"190 × 55 · 4 × Ø38") + [rect(208,34,190,55,rx=3),*bottle_holes(238,61.5,count,42,38),circle(220,61.5,6.4),circle(386,61.5,6.4)]
        g += part_label(208,104,"BACK",1,"190 × 95 · keeper mounts") + [rect(208,109,190,95,rx=3),circle(220,127,6.4),circle(386,127,6.4),line(218,189,388,189,"SCORE")]
        g += part_label(8,194,"STANDOFF",2,"70 × 22 · slots to calibrate") + [rect(8,199,70,22,rx=2),rect(88,199,70,22,rx=2)]
        bom = [
            {"part":"lower locating plate","qty":1,"size_mm":[190,70]},
            {"part":"base","qty":1,"size_mm":[190,55]},
            {"part":"upper keeper plate","qty":1,"size_mm":[190,55]},
            {"part":"back","qty":1,"size_mm":[190,95]},
            {"part":"standoff","qty":2,"size_mm":[70,22]},
            {"part":"M6 hand knob, bolt and washer set","qty":2,"size":"site-specific"},
        ]
        params.update({
            "keeper_type":"hand-knob-retained removable upper plate",
            "keeper_opening_diameter_mm":38.0,
            "cap_capture_per_side_mm":2.0,
            "interface_hole_mm":6.4,
            "assembly":"the lower plate locates each bottle body; the removable upper plate sits below the cap shoulder and is retained by two hand knobs",
            "mounting":"bench or approved wall backer",
            "service_sequence":["support bottles","remove two hand knobs","lift keeper plate","remove or replace bottles","refit plate and hand knobs","record fit and revision"],
            "physical_test_record_fields":["bottle body diameter","cap diameter","material thickness","opening fit","keeper height","knob clearance","load test","revision"],
            "safety":"The keeper is a serviceable anti-lift feature, not a child-resistant lock. Physically test access, load path and wall mounting before use.",
        })
    if kind != "captured-bottle-rack":
        g += [text(218,174,"CUT FILE CHECK",4,weight=700),text(218,181,"□ mm + viewBox",3.1),text(218,187,"□ one outline each",3.1),text(218,193,"□ test opening",3.1),text(218,199,"□ label parts",3.1)]
    return svg(kind.replace("-"," ").title(), "True-size reference parts for a configurable pill-bottle organizer.", 400, 225, g, {"project":"pill-bottle-organizer","design":kind,"parameters":params,"bom":bom}), params, bom


def exploded_diagram(kind: str) -> str:
    titles = {
        "simple-shelf-rack":"Simple shelf: shelf + sides + base",
        "dowel-supported-rack":"Dowel rack: top + dowels + bottom",
        "reinforced-wall-rack":"Wall rack: back + shelf + gussets",
        "removable-wall-bench-rack":"Transfer rack: shelf + back + interchangeable supports",
        "captured-bottle-rack":"Captured rack: base + locating plate + removable keeper",
    }
    body = [text(10,12,titles[kind],6,weight=700),text(10,20,"Exploded relationship diagram · arrows show assembly order, not scale",3.2,colour=GUIDE)]
    if kind == "simple-shelf-rack":
        body += [rect(55,35,120,40,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,55,4,29,22),rect(25,100,35,60,"ENGRAVE",colour="#546b7a"),rect(170,100,35,60,"ENGRAVE",colour="#546b7a"),rect(55,175,120,35,"ENGRAVE",colour="#546b7a"),text(115,94,"↓",10,"middle"),text(44,92,"↘",10,"middle"),text(188,92,"↙",10,"middle")]
    elif kind == "dowel-supported-rack":
        body += [rect(55,35,120,40,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,55,4,29,22),*[line(x,82,x,158,"ENGRAVE") for x in (62,168)],rect(55,165,120,40,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,185,4,29,22),text(115,123,"4 × DOWEL",4,"middle",700)]
    elif kind == "reinforced-wall-rack":
        body += [rect(55,35,120,80,"ENGRAVE",colour="#546b7a",rx=2),circle(72,50,5,"ENGRAVE"),circle(115,50,5,"ENGRAVE"),circle(158,50,5,"ENGRAVE"),rect(55,135,120,38,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,154,4,29,22),polygon([(30,135),(55,135),(55,110)],"ENGRAVE"),polygon([(175,135),(200,135),(175,110)],"ENGRAVE"),text(115,127,"↓ shelf",4,"middle")]
    elif kind == "removable-wall-bench-rack":
        body += [rect(55,35,120,45,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,57,4,29,22),rect(55,100,120,55,"ENGRAVE",colour="#546b7a",rx=2),text(115,94,"↓ MODULE",4,"middle",700),rect(15,185,90,28,"ENGRAVE",colour="#546b7a",rx=2),rect(125,185,90,28,"ENGRAVE",colour="#546b7a",rx=2),text(60,177,"BENCH FEET",3.5,"middle"),text(170,177,"WALL ADAPTER",3.5,"middle"),text(115,167,"choose one support",3.2,"middle",400,GUIDE)]
    else:
        body += [
            rect(55,34,120,32,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,50,4,29,24),
            text(115,76,"↓ removable keeper",3.6,"middle",700),
            *[rect(x,82,18,58,"ENGRAVE",colour="#9aa3ad",rx=5) for x in (64,93,122,151)],
            *[circle(x+9,87,22,"ENGRAVE",colour="#546b7a") for x in (64,93,122,151)],
            rect(55,146,120,32,"ENGRAVE",colour="#546b7a",rx=2),*bottle_holes(73,162,4,29,22),
            text(115,190,"↓ locating plate",3.6,"middle",700),rect(55,198,120,20,"ENGRAVE",colour="#546b7a",rx=2),
            line(45,36,45,64,"ENGRAVE"),circle(45,49,6.4,"ENGRAVE"),line(185,36,185,64,"ENGRAVE"),circle(185,49,6.4,"ENGRAVE"),
        ]
    body += [text(232,42,"ASSEMBLY REVIEW",4.5,weight=700),text(232,52,"1. Identify load path",3.2),text(232,60,"2. Confirm clearances",3.2),text(232,68,"3. Dry-fit first",3.2),text(232,76,"4. Check bottle removal",3.2),text(232,84,"5. Record revision",3.2),text(232,104,"STATUS: UNVERIFIED",3.4,weight=700,colour="#a33b2b")]
    return svg(f"{kind.replace('-',' ').title()} Exploded Diagram", "Teacher-facing assembly relationship diagram.", 340, 225, body, {"project":"pill-bottle-organizer","design":kind,"diagram":"exploded","physical_test_status":"unverified"})


def generate_examples() -> list[GeneratedFile]:
    files: list[GeneratedFile] = []
    designs: dict[str, object] = {}
    for design in ("simple-shelf-rack","dowel-supported-rack","reinforced-wall-rack","removable-wall-bench-rack","captured-bottle-rack"):
        parts, params, bom = example_sheet(design)
        parts_rel = f"pill-bottle/{design}/parts.svg"
        diagram_rel = f"pill-bottle/{design}/exploded.svg"
        write(parts_rel, parts)
        write(diagram_rel, exploded_diagram(design))
        files += [
            GeneratedFile(parts_rel, design.replace("-"," ").title(), "reference-assembly", "True-size reference parts; adapt measured parameters before cutting.", params),
            GeneratedFile(diagram_rel, f"{design.replace('-',' ').title()} Exploded Diagram", "teacher-diagram", "Assembly relationship diagram.", {"design":design}),
        ]
        designs[design] = {"files":{"parts":parts_rel,"exploded":diagram_rel},"parameters":params,"bom":bom,"assembly_notes":params["assembly"],"physical_test_status":"unverified"}
    write("pill-bottle/assemblies.json", json.dumps({"schema_version":1,"project":"pill-bottle-organizer","units":"mm","designs":designs},indent=2,sort_keys=True)+"\n")
    files.append(GeneratedFile("pill-bottle/assemblies.json", "Pill-Bottle Assembly Manifest", "manifest", "Parameters, BOMs, notes and verification status for five references.", {"design_count":5}))
    return files


def generate_standing_name_tag() -> list[GeneratedFile]:
    body = palette_header("STANDING NAME TAG COMPONENTS", "Choose and adapt a support concept; this sheet does not prescribe one finished stand.")
    body += [
        palette_card(8,34,96,60,"stand-triangle-leg","Triangle leg","50 × 50 · simple support",[polygon([(27,82),(77,82),(27,32)])],concept="triangle-leg"),
        palette_card(112,34,96,60,"stand-t-foot","T-foot","80 × 35 · slot to calibrate",[path("M 120 78 H 200 V 88 H 166 V 60 H 160 V 88 H 120 Z")],concept="t-foot",slot_width_mm=6),
        palette_card(8,102,96,60,"stand-cross-foot","Cross-foot pair","70 × 24 · half slots",[path("M 18 123 H 94 V 147 H 59 V 135 H 53 V 147 H 18 Z")],concept="cross-foot",slot_width_mm=6),
        palette_card(112,102,96,60,"stand-easel-leg","Easel back","70 × 18 · pivot Ø4",[rect(126,122,70,18,rx=3),circle(187,131,4)],concept="easel",pivot_mm=4),
    ]
    relative = "standing-name-tag/standing-name-tag-components.svg"
    write(relative, svg("Standing Name Tag Components", "Four adaptable support concepts for an open-ended stability investigation.",216,170,body,{"project":"make-it-stand","material_example_mm":6.0,"physical_test_status":"unverified"}))
    return [GeneratedFile(relative,"Standing Name Tag Components","component-set","Four support concepts for the standing-name-tag task.",{"concept_count":4})]


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    records = generate_palettes() + generate_individual_components() + generate_name_tag() + generate_standing_name_tag() + generate_examples()
    manifest = {
        "schema_version": 1,
        "title": "Technology Commons First Laser Projects Classroom Kit",
        "version": VERSION,
        "units": "mm",
        "license": "CC-BY-SA-4.0",
        "review_notice": "Software-checked does not mean physically tested. Every fabrication reference remains unverified until a recorded test.",
        "files": [record.__dict__ for record in records],
    }
    write("manifest.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    guide = """# First Laser Projects Classroom Kit

Use these files as measured building blocks, not finished answers. Open SVG files in Inkscape at 100%, confirm millimetres and document size, and edit a copy. Red lines communicate cut geometry; blue lines communicate score geometry. The machine operator still confirms the local mapping.

## Sequence

1. `name-tag/`: fit original name/logo artwork to a measured pre-cut blank and export PNG for engraving.
2. `standing-name-tag/`: choose and adapt a support concept, prototype it, then test stability.
3. `palettes/`: compare named geometry families. `components/` contains label-free exact-size files for direct import. A HOLE removes the inside of a closed path from a larger part; a CIRCLE PART keeps the disc.
4. `pill-bottle/`: compare four configurable assemblies. Measure the real bottle. The 34 mm body, 42 mm cap and 36 mm opening are documented example values—not universal bottle dimensions.

## Cut-readiness

- page units and display units are millimetres;
- width, height and `viewBox` agree;
- each intended outline appears once;
- fonts are not structurally critical;
- fit-sensitive geometry has a small physical test;
- mounting and load-bearing designs have instructor approval;
- the physical-test status is recorded honestly.
"""
    write("README.md", guide)
    checksum_paths = sorted(
        (p for p in OUT.rglob("*") if p.is_file() and p.name not in {"SHA256SUMS", "technology-commons-first-laser-projects.zip"}),
        key=lambda p: p.relative_to(OUT).as_posix(),
    )
    write("SHA256SUMS", "\n".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(OUT).as_posix()}" for p in checksum_paths) + "\n")
    archive_path = OUT / "technology-commons-first-laser-projects.zip"
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_STORED) as archive:
        archive_items = sorted(
            (p for p in OUT.rglob("*") if p.is_file() and p != archive_path),
            key=lambda p: p.relative_to(OUT).as_posix(),
        )
        for item in archive_items:
            info = zipfile.ZipInfo((Path("technology-commons-first-laser-projects") / item.relative_to(OUT)).as_posix(), date_time=(2026,1,1,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_STORED
            payload = item.read_bytes()
            if item.suffix.lower() in {".csv", ".json", ".md", ".svg", ".txt", ".yml", ".yaml"} or item.name == "SHA256SUMS":
                payload = payload.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            archive.writestr(info, payload)
    print(f"Generated classroom kit with {len(records)} documented files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
