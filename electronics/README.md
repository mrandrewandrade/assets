# TEJ electronics asset library

This directory is the canonical source for original TEJ electronics teaching artifacts.

## Structure

- `reference/`: formula and calculator references
- `worksheets/`: maintainable student worksheets and teacher keys
- `modules/`: complete hardware-module packages
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

The command renders seven PDFs and one HTML reference into `dist/`. XeLaTeX is required for the PDF build. Rendered outputs use stable, descriptive filenames.

## Copyright boundary

Do not add copyrighted textbook PDFs to this repository. Keep complete books and permitted chapter extracts in restricted Google Drive and record only titles, citations, access category, and Drive links in manifests.
