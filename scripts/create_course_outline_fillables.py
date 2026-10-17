from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, DecodedStreamObject, NameObject
from reportlab.lib.colors import black, white
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tmp" / "pdfs" / "course-outlines"
OUTPUT_DIR = ROOT / "output" / "pdf"


@dataclass(frozen=True)
class Outline:
    code: str
    source_name: str
    output_name: str
    title: str


OUTLINES = (
    Outline(
        code="TAS2O",
        source_name="tas2o-source.pdf",
        output_name="2026-27_TAS2O_Course_Outline_Fillable.pdf",
        title="2026-27 TAS2O Technology and the Skilled Trades - Fillable Course Outline",
    ),
    Outline(
        code="TEJ3M",
        source_name="tej3m-source.pdf",
        output_name="2026-27_TEJ3M_Course_Outline_Fillable.pdf",
        title="2026-27 TEJ3M Computer Engineering Technology - Fillable Course Outline",
    ),
    Outline(
        code="TTS3C",
        source_name="tts3c-source.pdf",
        output_name="2026-27_TTS3C_Course_Outline_Fillable.pdf",
        title="2026-27 TTS3C Small Engine and Recreational Equipment - Fillable Course Outline",
    ),
)

FIELD_NAMES = (
    "signature_date",
    "caregiver_guardian_signature",
    "student_name_and_number",
    "student_signature",
)

# ReportLab adds a small internal left inset to text fields. Extending the
# widget two points to the left makes entered text begin at the printed line.
TEXT_FIELD_LEFT_COMPENSATION = 2.0


def find_signature_lines(source: Path) -> tuple[int, float, float, list[tuple[float, float, float, float]]]:
    with pdfplumber.open(source) as pdf:
        page_index = len(pdf.pages) - 1
        page = pdf.pages[page_index]
        lines = [
            (float(w["x0"]), float(w["x1"]), float(w["top"]), float(w["bottom"]))
            for w in page.extract_words()
            if len(w["text"]) >= 20 and set(w["text"]) == {"_"}
        ]
        lines.sort(key=lambda item: (item[2], item[0]))
        if len(lines) != 4:
            raise ValueError(f"Expected four acknowledgment lines in {source.name}; found {len(lines)}")
        return page_index, float(page.width), float(page.height), lines


def add_text_field(
    c: canvas.Canvas,
    *,
    name: str,
    x0: float,
    x1: float,
    top: float,
    bottom: float,
    page_height: float,
) -> None:
    height = max(15.0, bottom - top + 4.0)
    c.acroForm.textfield(
        name=name,
        tooltip=name.replace("_", " ").title(),
        x=x0 - TEXT_FIELD_LEFT_COMPENSATION,
        y=page_height - bottom - 2.0,
        width=x1 - x0 + TEXT_FIELD_LEFT_COMPENSATION,
        height=height,
        borderWidth=0,
        borderColor=white,
        fillColor=None,
        textColor=black,
        forceBorder=True,
        fontName="Helvetica",
        fontSize=11.5,
    )


def make_overlay(source: Path, overlay: Path) -> tuple[int, list[str]]:
    page_index, page_width, page_height, lines = find_signature_lines(source)
    source_reader = PdfReader(str(source))
    c = canvas.Canvas(str(overlay), pagesize=(page_width, page_height))

    for _ in range(page_index):
        c.showPage()

    for name, (x0, x1, top, bottom) in zip(FIELD_NAMES, lines):
        add_text_field(
            c,
            name=name,
            x0=x0,
            x1=x1,
            top=top,
            bottom=bottom,
            page_height=page_height,
        )
    c.save()

    if len(source_reader.pages) != page_index + 1:
        raise ValueError("Unexpected source page count")
    return page_index, list(FIELD_NAMES)


def strip_text_field_backgrounds(writer: PdfWriter) -> None:
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


def merge_source_with_fields(source: Path, overlay: Path, output: Path, title: str) -> None:
    source_reader = PdfReader(str(source))
    overlay_reader = PdfReader(str(overlay))
    if len(source_reader.pages) != len(overlay_reader.pages):
        raise ValueError(f"Page mismatch for {source.name}")

    writer = PdfWriter()
    writer.clone_document_from_reader(overlay_reader)
    writer.add_metadata(
        {
            "/Title": title,
            "/Author": "Port Credit Secondary School",
            "/Subject": "Course outline and guardian-student acknowledgment",
            "/Creator": "Port Credit Secondary School",
        }
    )
    for index, source_page in enumerate(source_reader.pages):
        empty = DecodedStreamObject()
        empty.set_data(b"")
        writer.pages[index][NameObject("/Contents")] = writer._add_object(empty)
        writer.pages[index].merge_page(source_page, over=True)

    strip_text_field_backgrounds(writer)
    acro = writer.root_object.get("/AcroForm")
    if acro is not None:
        acro.get_object()[NameObject("/NeedAppearances")] = BooleanObject(False)
    with output.open("wb") as stream:
        writer.write(stream)


def effective_value(widget):
    if "/V" in widget:
        return widget.get("/V")
    parent = widget.get("/Parent")
    if parent is not None:
        return parent.get_object().get("/V")
    return None


def validate_interactive(path: Path, expected_names: list[str], expected_values=None) -> None:
    reader = PdfReader(str(path))
    fields = reader.get_fields() or {}
    if set(fields) != set(expected_names):
        raise ValueError(
            f"Field mismatch in {path.name}. Missing={sorted(set(expected_names) - set(fields))} "
            f"Extra={sorted(set(fields) - set(expected_names))}"
        )

    widget_names: list[str] = []
    for page in reader.pages:
        for annot_ref in page.get("/Annots", []):
            annot = annot_ref.get_object()
            if annot.get("/Subtype") != "/Widget":
                continue
            parent_ref = annot.get("/Parent")
            parent = parent_ref.get_object() if parent_ref is not None else None
            name = annot.get("/T") or (parent.get("/T") if parent else None)
            if name:
                widget_names.append(str(name))
            appearance = annot.get("/AP")
            if appearance is None or appearance.get("/N") is None:
                raise ValueError(f"Widget {name} has no normal appearance")
            normal = appearance.get("/N").get_object()
            if not bool(normal.get_data()):
                raise ValueError(f"Widget {name} has an empty appearance stream")
            if expected_values and name in expected_values:
                actual = effective_value(annot)
                if str(actual) != str(expected_values[name]):
                    raise ValueError(f"Widget value mismatch for {name}: {actual!r}")

    if sorted(widget_names) != sorted(expected_names):
        raise ValueError(f"Widget names do not match canonical fields in {path.name}")

    if expected_values:
        for name, expected in expected_values.items():
            actual = fields[name].get("/V")
            if str(actual) != str(expected):
                raise ValueError(f"Canonical value mismatch for {name}: {actual!r}")


def make_test_fill(final: Path, test_filled: Path, expected_names: list[str]) -> None:
    sample = {
        "signature_date": "2026-10-12",
        "caregiver_guardian_signature": "Sample Caregiver",
        "student_name_and_number": "Sample Student, 123456789",
        "student_signature": "Sample Student",
    }
    reader = PdfReader(str(final))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    writer.update_page_form_field_values(None, sample, auto_regenerate=False)
    with test_filled.open("wb") as stream:
        writer.write(stream)
    validate_interactive(test_filled, expected_names, sample)


def build(outline: Outline) -> None:
    source = SOURCE_DIR / outline.source_name
    overlay = SOURCE_DIR / f"{outline.code.lower()}-fields-overlay.pdf"
    final = OUTPUT_DIR / outline.output_name
    test_filled = SOURCE_DIR / f"{outline.code.lower()}-test-filled.pdf"

    page_index, expected_names = make_overlay(source, overlay)
    merge_source_with_fields(source, overlay, final, outline.title)
    validate_interactive(final, expected_names)
    make_test_fill(final, test_filled, expected_names)
    print(f"Created {final}")
    print(f"Validated {len(expected_names)} fields on page {page_index + 1}")
    print(f"Created and validated sample fill {test_filled}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build fillable course-outline PDFs")
    parser.add_argument(
        "codes",
        nargs="*",
        choices=[outline.code for outline in OUTLINES],
        help="Course codes to build. If omitted, all outlines are built.",
    )
    args = parser.parse_args()
    selected = set(args.codes)

    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for outline in OUTLINES:
        if not selected or outline.code in selected:
            build(outline)


if __name__ == "__main__":
    main()
