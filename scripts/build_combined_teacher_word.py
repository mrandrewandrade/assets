#!/usr/bin/env python3
"""Generate the editable combined teacher marking DOCX using only Python stdlib."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assignments" / "combined-teacher-marking.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def run(text, *, bold=False, size=16, color=None):
    props = []
    if bold:
        props.append("<w:b/>")
    props.append(f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>')
    props.append('<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial"/>')
    if color:
        props.append(f'<w:color w:val="{color}"/>')
    return f"<w:r><w:rPr>{''.join(props)}</w:rPr><w:t xml:space=\"preserve\">{escape(text)}</w:t></w:r>"


def paragraph(parts=None, *, before=0, after=0, align=None, keep=False, page_break=False):
    ppr = [f'<w:spacing w:before="{before}" w:after="{after}"/>']
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if keep:
        ppr.append("<w:keepNext/>")
    body = ""
    if page_break:
        body = "<w:r><w:br w:type=\"page\"/></w:r>"
    elif parts:
        body = "".join(parts)
    return f"<w:p><w:pPr>{''.join(ppr)}</w:pPr>{body}</w:p>"


def cell(text, width, *, bold=False, fill=None, color=None, align="left", size=15):
    tcpr = [f'<w:tcW w:w="{width}" w:type="dxa"/>', '<w:vAlign w:val="center"/>']
    if fill:
        tcpr.append(f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>')
    content = paragraph([run(text, bold=bold, size=size, color=color)], align=align, after=0)
    return f"<w:tc><w:tcPr>{''.join(tcpr)}</w:tcPr>{content}</w:tc>"


def row(values, widths, *, header=False, height=410):
    cells = []
    for i, value in enumerate(values):
        align = "center" if i in (2, 4) else "left"
        cells.append(
            cell(
                value,
                widths[i],
                bold=header,
                fill="1E2B55" if header else None,
                color="FFFFFF" if header else None,
                align=align,
                size=14 if header else 14,
            )
        )
    trpr = f'<w:trPr><w:cantSplit/><w:trHeight w:val="{height}" w:hRule="atLeast"/></w:trPr>'
    return f"<w:tr>{trpr}{''.join(cells)}</w:tr>"


def table(start, end):
    widths = [1350, 3150, 750, 3000, 750, 4850]
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)
    borders = "".join(
        f'<w:{side} w:val="single" w:sz="4" w:space="0" w:color="D9DEE2"/>'
        for side in ("top", "left", "bottom", "right", "insideH", "insideV")
    )
    props = (
        '<w:tblPr>'
        '<w:tblW w:w="13850" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        f'<w:tblBorders>{borders}</w:tblBorders>'
        '<w:tblCellMar>'
        '<w:top w:w="40" w:type="dxa"/><w:left w:w="55" w:type="dxa"/>'
        '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="55" w:type="dxa"/>'
        '</w:tblCellMar>'
        '</w:tblPr>'
    )
    rows = [row(["Student", "Presentation scores", "P /10", "Listening flags", "L /10", "Learning Skills / quick note"], widths, header=True, height=430)]
    for n in range(start, end + 1):
        rows.append(
            row(
                [
                    f"{n}.",
                    "K ___  T ___  C ___  V ___  A ___",
                    "",
                    "PH [ ]  TK [ ]  OF [ ]  NN [ ]  PR [ ]",
                    "",
                    "",
                ],
                widths,
                height=405,
            )
        )
    return f"<w:tbl>{props}<w:tblGrid>{grid}</w:tblGrid>{''.join(rows)}</w:tbl>"


def page_intro(title_suffix):
    return "".join(
        [
            paragraph([run("Combined Teacher Marking", bold=True, size=34, color="1E2B55")], after=40, keep=True),
            paragraph([run(f"Past, Present & Becoming + The Way We Meet - {title_suffix}", size=17, color="596673")], after=70, keep=True),
            paragraph(
                [
                    run("Presentation: ", bold=True, size=14, color="1E2B55"),
                    run("K Knowledge, T Thinking, C Communication, V Visuals/accessibility, A Application, each /2. P = presentation /10.", size=14),
                ],
                after=25,
            ),
            paragraph(
                [
                    run("Listening flags: ", bold=True, size=14, color="1E2B55"),
                    run("PH phone, TK talking/side conversation, OF off-task/not facing, NN not taking notes, PR prompted/reminded. Mark only when observed. L = listening /10 after checking submitted notes/photos and self-evaluation.", size=14),
                ],
                after=25,
            ),
            paragraph(
                [
                    run("LS: ", bold=True, size=14, color="1E2B55"),
                    run("R Responsibility, O Organization, IW Independent Work, C Collaboration, I Initiative, SR Self-Regulation. Blank listening flags mean no concern was observed, not proof of perfect attention.", size=14),
                ],
                after=55,
            ),
        ]
    )


def document_xml():
    body = []
    body.append(page_intro("Students 1-17"))
    body.append(table(1, 17))
    body.append(paragraph(page_break=True))
    body.append(page_intro("Students 18-34"))
    body.append(table(18, 34))
    body.append(
        f'''<w:sectPr>
        <w:footerReference w:type="default" r:id="rId1"/>
        <w:pgSz w:w="15840" w:h="12240" w:orient="landscape"/>
        <w:pgMar w:top="432" w:right="432" w:bottom="500" w:left="432" w:header="250" w:footer="250" w:gutter="0"/>
        <w:cols w:space="720"/>
        <w:docGrid w:linePitch="360"/>
        </w:sectPr>'''
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="{W}" xmlns:r="{R}"><w:body>{''.join(body)}</w:body></w:document>'''


def footer_xml():
    text = "CC BY 4.0 - share and adapt with attribution to Andrew Andrade: https://github.com/mrandrewandrade"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="{W}" xmlns:r="{R}">{paragraph([run(text, size=12, color="596673")], align="center")}</w:ftr>'''


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>'''

STYLES = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="{W}">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="16"/><w:szCs w:val="16"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:after="0"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
</w:styles>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Combined Teacher Marking</dc:title>
  <dc:creator>Andrew Andrade</dc:creator>
  <cp:lastModifiedBy>Andrew Andrade</cp:lastModifiedBy>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Technology Commons resource builder</Application>
</Properties>'''


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", document_xml())
        z.writestr("word/styles.xml", STYLES)
        z.writestr("word/footer1.xml", footer_xml())
        z.writestr("word/_rels/document.xml.rels", DOC_RELS)
        z.writestr("docProps/core.xml", CORE)
        z.writestr("docProps/app.xml", APP)
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
