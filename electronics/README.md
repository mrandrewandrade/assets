# TEJ electronics asset library

This directory is the canonical source for original TEJ electronics teaching artifacts.

Use [MODULE-DEVELOPMENT-SOP.md](MODULE-DEVELOPMENT-SOP.md) when creating or revising a coordinated lesson package. It defines the Google Slides teaching deck, handwritten-work submission Google Doc, restricted worked-answer Google Doc, schematic workflow, alignment rules, and release checks. The Basic Electricity to Basic Computer Systems package is the reference implementation.

Use the [cheat sheet and reference guide style guide](styles/cheat-sheet-reference-guide-style-guide.md) for printable formula sheets, quick references, and compact reference guides. It defines typography, tables, equation spacing, schematic rules, print constraints, and measurable no-overlap checks.

## Structure

- `reference/`: the printable quick reference and the single curriculum-ordered course book
- `worksheets/`: maintainable student worksheets and teacher keys
- `modules/`: complete hardware-module packages
- `computer-systems/`: CS01-CS08 Main Quest and SQ01-SQ06 Side Quest activity packages
- `schematics/`: reusable accessible SVG diagrams
- `templates/`: student, key, lab, and metadata templates
- `metadata/`: machine-readable asset records and schema
- `references/`: manifests for restricted and open sources, never copyrighted textbook bytes
- `styles/`: shared LaTeX and HTML styles

## Build

From the repository root:

```bash
bash render.sh electronics
```

On Windows PowerShell when Git Bash or WSL is unavailable:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/render-electronics.ps1
```

The command renders the maintained student, teacher, reference, and module PDFs plus the self-contained handbook HTML into `dist/`. XeLaTeX is required for the PDF build. CircuitikZ and TikZ sources generate the reusable PDF and SVG diagrams.

Main Quest and Side Quest classification for the computer-systems layer is maintained in `metadata/computer-systems.yml`. Student pages, teacher guidance, website labels, and Classroom posting language should use the `pathway` field instead of inventing a second classification.

## Copyright boundary

Do not add copyrighted textbook PDFs to this repository. Keep complete books and permitted chapter extracts in restricted Google Drive and record only titles, citations, access category, and Drive links in manifests.
