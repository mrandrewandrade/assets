from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, DecodedStreamObject, NameObject
from reportlab.lib.colors import black, white
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "tmp" / "pdfs" / "personal-items" / "source.pdf"
OVERLAY = ROOT / "tmp" / "pdfs" / "personal-items" / "fields-overlay.pdf"
FINAL = ROOT / "output" / "pdf" / "Personal_Items_Brought_to_Technology_Class_Fillable.pdf"
TEST_FILLED = ROOT / "tmp" / "pdfs" / "personal-items" / "test-filled.pdf"

PAGE_W = 612
PAGE_H = 792
TEXT_FIELD_LEFT_COMPENSATION = 2.0
PAGE1_FIELD_VERTICAL_SHIFT = 1.75
PAGE2_FIELD_VERTICAL_SHIFT = -20.0


def y_from_top(bottom: float, height: float = 15.0) -> float:
    return PAGE_H - bottom - 2.0


def add_text(c: canvas.Canvas, name: str, x0: float, x1: float, top: float, bottom: float,
             *, multiline: bool = False, height: float | None = None) -> None:
    h = height if height is not None else max(15.0, bottom - top + 4.0)
    y = PAGE_H - bottom - 2.0
    flags = 4096 if multiline else 0
    c.acroForm.textfield(
        name=name,
        tooltip=name.replace("_", " ").title(),
        x=x0 - TEXT_FIELD_LEFT_COMPENSATION,
        y=y,
        width=x1 - x0 + TEXT_FIELD_LEFT_COMPENSATION,
        height=h,
        borderWidth=0,
        borderColor=white,
        fillColor=None,
        textColor=black,
        forceBorder=True,
        fontName="Helvetica",
        fontSize=11.5,
        fieldFlags=flags,
    )


def add_checkbox(c: canvas.Canvas, name: str, x: float, bottom: float, size: float = 8.2) -> None:
    c.acroForm.checkbox(
        name=name,
        tooltip=name.replace("_", " ").title(),
        x=x - 0.5,
        y=PAGE_H - bottom + 1.6,
        size=size,
        checked=False,
        buttonStyle="check",
        borderWidth=0.7,
        borderColor=black,
        fillColor=white,
        textColor=black,
        forceBorder=True,
    )


def make_overlay() -> list[str]:
    OVERLAY.parent.mkdir(parents=True, exist_ok=True)
    FINAL.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OVERLAY), pagesize=(PAGE_W, PAGE_H))
    names: list[str] = []

    page1_text = [
        ("student_number", 131.5, 357.7, 480.97, 492.27, False, None),
        ("student_name", 119.6, 352.1, 497.89, 509.19, False, None),
        ("parent_guardian", 142.9, 343.9, 514.82, 526.12, False, None),
        ("parent_contact", 398.5, 530.5, 514.82, 526.12, False, None),
        ("item_description", 129.0, 531.1, 531.74, 543.04, False, None),
        ("make_model", 110.8, 355.8, 548.66, 559.96, False, None),
        ("serial_number", 441.9, 536.1, 548.66, 559.96, False, None),
        ("intended_date_to_bring", 200.6, 382.8, 565.59, 576.89, False, None),
        ("activity_other_text", 364.2, 439.6, 613.86, 625.16, False, None),
        ("known_defects_hazards", 43.0, 545.6, 660.0, 691.0, True, 34.0),
    ]
    for args in page1_text:
        shifted = (*args[:3], args[3] + PAGE1_FIELD_VERTICAL_SHIFT, args[4] + PAGE1_FIELD_VERTICAL_SHIFT)
        add_text(c, *shifted, multiline=args[5], height=args[6])
        names.append(args[0])

    page1_checks = [
        ("activity_inspection", 137.2, 608.23),
        ("activity_demonstration", 208.1, 608.23),
        ("activity_repair_attempt", 300.9, 608.23),
        ("activity_project_use", 108.9, 625.16),
        ("activity_donation", 184.8, 625.16),
        ("activity_other", 319.7, 625.16),
    ]
    for name, x, bottom in page1_checks:
        add_checkbox(c, name, x, bottom + PAGE1_FIELD_VERTICAL_SHIFT)
        names.append(name)
    c.showPage()

    page2_text = [
        ("student_name_ack", 117.6, 343.7, 496.75, 507.75, False, None),
        ("student_signature", 135.3, 343.1, 525.67, 536.67, False, None),
        ("student_date", 381.6, 510.0, 525.67, 536.67, False, None),
        ("parent_guardian_name", 170.7, 341.9, 620.46, 631.46, False, None),
        ("parent_guardian_signature", 96.2, 352.9, 649.39, 660.39, False, None),
        ("parent_guardian_date", 391.4, 519.8, 649.39, 660.39, False, None),
    ]
    for args in page2_text:
        shifted = (*args[:3], args[3] + PAGE2_FIELD_VERTICAL_SHIFT, args[4] + PAGE2_FIELD_VERTICAL_SHIFT)
        add_text(c, *shifted, multiline=args[5], height=args[6])
        names.append(args[0])
    c.save()
    return names


def merge_source_with_fields() -> None:
    source = PdfReader(str(SOURCE))
    overlay = PdfReader(str(OVERLAY))
    if len(source.pages) != 2 or len(overlay.pages) != 2:
        raise ValueError("Expected exactly two source and overlay pages")

    writer = PdfWriter()
    writer.clone_document_from_reader(overlay)
    writer.add_metadata({
        "/Title": "Personal Items Brought to Technology Class - Fillable Acknowledgment",
        "/Author": "Port Credit Secondary School",
        "/Subject": "Acknowledgment of risk and safety expectations for personal items brought to technology class",
        "/Creator": "Port Credit Secondary School",
    })
    for index, source_page in enumerate(source.pages):
        empty = DecodedStreamObject()
        empty.set_data(b"")
        writer.pages[index][NameObject("/Contents")] = writer._add_object(empty)
        writer.pages[index].merge_page(source_page, over=True)
    for page in writer.pages:
        for annot_ref in page.get("/Annots", []):
            annot = annot_ref.get_object()
            parent_ref = annot.get("/Parent")
            parent = parent_ref.get_object() if parent_ref is not None else None
            field_type = annot.get("/FT") or (parent.get("/FT") if parent else None)
            if field_type != "/Tx":
                continue
            mk = annot.get("/MK")
            if mk is not None:
                mk.get_object().pop(NameObject("/BG"), None)
            normal = annot.get("/AP", {}).get("/N")
            if normal is not None:
                stream = normal.get_object()
                lines = stream.get_data().splitlines(keepends=True)
                if len(lines) >= 3 and lines[0].rstrip().endswith(b"rg") and lines[2].strip() == b"f":
                    stream.set_data(b"".join(lines[3:]))
    acro = writer.root_object.get("/AcroForm")
    if acro is not None:
        acro_obj = acro.get_object()
        acro_obj[NameObject("/NeedAppearances")] = BooleanObject(False)
    with FINAL.open("wb") as stream:
        writer.write(stream)


def effective_value(widget):
    if "/V" in widget:
        return widget.get("/V")
    parent = widget.get("/Parent")
    if parent is not None:
        return parent.get_object().get("/V")
    return None


def validate_interactive(expected_names: list[str], path: Path, expected_values=None) -> None:
    reader = PdfReader(str(path))
    fields = reader.get_fields() or {}
    missing = set(expected_names) - set(fields)
    extra = set(fields) - set(expected_names)
    if missing or extra:
        raise ValueError(f"Field mismatch. Missing={sorted(missing)} Extra={sorted(extra)}")

    widget_names = []
    for page in reader.pages:
        for annot_ref in page.get("/Annots", []):
            annot = annot_ref.get_object()
            if annot.get("/Subtype") != "/Widget":
                continue
            parent = annot.get("/Parent")
            parent_obj = parent.get_object() if parent is not None else None
            name = annot.get("/T") or (parent_obj.get("/T") if parent_obj else None)
            if name:
                widget_names.append(str(name))
            ap = annot.get("/AP")
            if ap is None or ap.get("/N") is None:
                raise ValueError(f"Widget {name} has no normal appearance")
            normal = ap.get("/N")
            normal_obj = normal.get_object() if hasattr(normal, "get_object") else normal
            if hasattr(normal_obj, "get_data"):
                if not bool(normal_obj.get_data()):
                    raise ValueError(f"Widget {name} has an empty appearance stream")
            elif isinstance(normal_obj, dict):
                streams = [v.get_object() for v in normal_obj.values()]
                if not streams or not any(bool(getattr(s, "get_data", lambda: b"")()) for s in streams):
                    raise ValueError(f"Widget {name} has empty checkbox appearances")
            else:
                raise ValueError(f"Widget {name} has an empty appearance stream")

            if expected_values and name in expected_values:
                value = effective_value(annot)
                if str(value) != str(expected_values[name]):
                    raise ValueError(f"Widget value mismatch for {name}: {value!r}")
    if sorted(widget_names) != sorted(expected_names):
        raise ValueError("Widget names do not match canonical field names")

    if expected_values:
        for name, expected in expected_values.items():
            actual = fields[name].get("/V")
            if str(actual) != str(expected):
                raise ValueError(f"Canonical value mismatch for {name}: {actual!r}")


def make_test_fill(expected_names: list[str]) -> None:
    sample = {
        "student_number": "123456789",
        "item_description": "Small project item",
        "intended_date_to_bring": "2026-10-12",
        "activity_project_use": "/Yes",
        "student_name": "Sample Student",
        "student_name_ack": "Sample Student",
        "student_signature": "Sample Student",
        "student_date": "2026-10-12",
    }
    reader = PdfReader(str(FINAL))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.update_page_form_field_values(None, sample, auto_regenerate=False)
    with TEST_FILLED.open("wb") as stream:
        writer.write(stream)
    validate_interactive(expected_names, TEST_FILLED, sample)


def main() -> None:
    expected_names = make_overlay()
    if len(expected_names) != len(set(expected_names)):
        raise ValueError("Duplicate field names")
    merge_source_with_fields()
    validate_interactive(expected_names, FINAL)
    make_test_fill(expected_names)
    print(f"Created {FINAL}")
    print(f"Validated {len(expected_names)} canonical fields and widgets")
    print(f"Created and validated sample fill {TEST_FILLED}")


if __name__ == "__main__":
    main()
