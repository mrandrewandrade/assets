#!/usr/bin/env python3
"""Build branded teaching documents from Markdown to HTML and PDF."""

from __future__ import annotations

import base64
import re
import sys
from datetime import date
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / "assignments"
DIST = ROOT / "dist"
TEMPLATES = ROOT / "templates"
BRAND = ROOT / "brand"

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n(.*)\Z", re.DOTALL)


def read_source(path: Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    match = FRONT_MATTER.match(raw)
    if not match:
        raise ValueError(f"{path} must start with YAML front matter")
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, match.group(2)


def logo_data_uri() -> str:
    data = (BRAND / "aa-logo.svg").read_bytes()
    encoded = base64.b64encode(data).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def combined_css() -> str:
    tokens = (BRAND / "tokens.css").read_text(encoding="utf-8")
    stylesheet = (TEMPLATES / "assignment.css").read_text(encoding="utf-8")
    stylesheet = re.sub(r'^@import url\("\.\./brand/tokens\.css"\);\s*', "", stylesheet)
    return tokens + "\n" + stylesheet


def write_pdf(html_path: Path, pdf_path: Path) -> None:
    generated = date.today().isoformat()
    footer = f"""
    <div style="width:100%; padding:0 0.58in; font-family:Arial,Helvetica,sans-serif;
                font-size:7.5pt; color:#66717B; display:flex; justify-content:space-between;">
      <span>{pdf_path.name} · generated {generated}</span>
      <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
    </div>
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
        page.emulate_media(media="print")
        page.pdf(
            path=str(pdf_path),
            print_background=True,
            prefer_css_page_size=True,
            display_header_footer=True,
            header_template="<span></span>",
            footer_template=footer,
        )
        browser.close()


def render(path: Path) -> tuple[Path, Path]:
    meta, body = read_source(path)

    title = meta.get("title", path.stem.replace("-", " ").title())
    subtitle = meta.get("subtitle", "")
    document_type = meta.get("document_type", "Assignment")
    slug = meta.get("slug", path.stem)

    content = markdown.markdown(
        body,
        extensions=["tables", "sane_lists", "fenced_code", "md_in_html"],
        output_format="html5",
    )

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("assignment.html")
    html = template.render(
        title=title,
        subtitle=subtitle,
        document_type=document_type,
        content=content,
        css=combined_css(),
        logo_data_uri=logo_data_uri(),
    )

    DIST.mkdir(parents=True, exist_ok=True)
    html_path = DIST / f"{slug}.html"
    pdf_path = DIST / f"{slug}.pdf"

    html_path.write_text(html, encoding="utf-8")
    write_pdf(html_path, pdf_path)

    return html_path, pdf_path


def sources_from_args(args: list[str]) -> list[Path]:
    if not args:
        return sorted(ASSIGNMENTS.glob("*.md"))

    sources = []
    for value in args:
        path = Path(value)
        if not path.is_absolute():
            path = ROOT / path
        sources.append(path.resolve())
    return sources


def main() -> int:
    sources = sources_from_args(sys.argv[1:])
    if not sources:
        print("No assignment Markdown files found.")
        return 1

    for source in sources:
        html_path, pdf_path = render(source)
        print(f"Built {html_path.relative_to(ROOT)}")
        print(f"Built {pdf_path.relative_to(ROOT)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
