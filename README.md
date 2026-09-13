# Assets

Reusable branded teaching documents and source assets for Andrew Andrade's Technology Commons materials.

The goal of this repository is to keep student-facing documents simple, accessible, reproducible, and easy to revise. Assignment PDFs are generated from Markdown using a shared HTML/CSS template rather than being hand-formatted one at a time.

## Design principles

The document system follows a restrained, Tufte-inspired approach:

- strong hierarchy, generous whitespace, and minimal decoration
- information first, branding second
- high contrast and readable type
- colour used sparingly and meaningfully
- thin rules instead of heavy boxes
- tables designed for scanning, not visual noise
- source content stays in Markdown

The visual tokens are adapted from the Technology Commons brand kit in `mrandrewandrade/commons`, using Sail White, Lighthouse Black, Port Credit Navy, Technical Blue, and PCSS Gold.

## Repository structure

```text
assignments/          Markdown source for individual assignments
brand/                Reusable brand tokens and logo
scripts/              PDF build tooling
templates/            Shared document template and print stylesheet
dist/                 Generated output, not committed
```

## Build

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/build.py
```

Build one document:

```bash
python scripts/build.py assignments/about-me-presentation.md
```

Generated PDFs and HTML previews are written to `dist/`.

A GitHub Actions workflow also builds the PDFs and uploads them as a workflow artifact on pushes and pull requests.

## Creating a new assignment

1. Copy an existing Markdown file in `assignments/`.
2. Change the YAML front matter and student-facing content.
3. Keep rubric columns in this order when used: `Category | 4+ | Level 4 | Level 3 | Level 2 | Level 1`.
4. Use `<div class="page-break"></div>` when a clean page break is needed.
5. Run the build and inspect the PDF before posting it for students.

## Licensing

Unless a file says otherwise, original material in this repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You may share and adapt the material, including commercially, as long as you provide appropriate attribution, link to the licence, and indicate whether changes were made.

Suggested attribution:

> Technology Commons teaching materials by Andrew Andrade, licensed under CC BY 4.0. Source: https://github.com/mrandrewandrade/assets

For an adaptation:

> Adapted from Technology Commons teaching materials by Andrew Andrade, licensed under CC BY 4.0. Changes were made. Source: https://github.com/mrandrewandrade/assets

See [LICENSE.md](LICENSE.md) for the licence notice and canonical licence link.
