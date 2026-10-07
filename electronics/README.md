# TEJ electronics asset library

This directory is the canonical source for original TEJ electronics teaching artifacts.

Use [MODULE-DEVELOPMENT-SOP.md](MODULE-DEVELOPMENT-SOP.md) when creating or revising a complete module. It defines the instructional sequence, required student and teacher materials, schematic workflow, alignment rules, and release checks. H01 Safety and Lab Practice is the reference implementation.

## Structure

- `reference/`: the two-page quick reference and curriculum-ordered handbook
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
