# Assets

Reusable branded teaching documents and source assets for Andrew Andrade's Technology Commons materials.

The goal of this repository is to keep student-facing documents simple, accessible, reproducible, and easy to revise. Current assignment PDFs are authored as Quarto documents and rendered with Typst.

## Design principles

The document system follows a restrained, Tufte-inspired approach:

- strong hierarchy, generous whitespace, and minimal decoration
- information first, branding second
- high contrast and readable type
- colour used sparingly and meaningfully
- thin rules instead of heavy boxes
- tables designed for scanning, not visual noise
- source content stays editable and version controlled

The visual tokens are adapted from the Technology Commons brand kit in `mrandrewandrade/commons`.

## Repository structure

```text
assignments/          Quarto/Typst assignment sources and assignment assets
brand/                Reusable brand assets
templates/            Legacy HTML/CSS document template
scripts/              Build and setup tooling
dist/                 Generated output, not committed
```

## Windows setup

The current PDF toolchain requires Quarto. Typst is bundled with Quarto, so Typst does not need to be installed separately.

From Git Bash, run:

```bash
bash scripts/setup-windows.sh
```

If Quarto is not installed, the script will show the Windows install command:

```bash
winget install --id Posit.Quarto -e
```

After installing Quarto, close and reopen Git Bash, then run the setup script again.

You can also verify the toolchain directly:

```bash
quarto --version
quarto typst --version
quarto check
```

## Build the About Me PDF

From the repository root:

```bash
bash render.sh about-me
```

The generated PDF is written to:

```text
dist/about-me-presentation.pdf
```

The underlying source is:

```text
assignments/about-me-presentation.qmd
```

The GitHub Actions workflow uses the same Quarto/Typst rendering path and uploads the generated files in `dist/` as a workflow artifact.

## Creating another assignment

For the current document system, use the existing `.qmd` assignment as a starting point and keep reusable images or branding in the appropriate asset folder. Add a matching command to `render.sh` when the assignment is ready to become part of the standard build.

## Legacy renderer

The repository still contains the earlier Markdown, HTML/CSS, Python, and Playwright renderer. Those files are retained for reference, but the About Me PDF and current GitHub Actions build use Quarto and Typst.

## Licensing

Unless a file says otherwise, original material in this repository is licensed under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**.

You may share and adapt the material, including commercially, as long as you provide appropriate attribution, link to the licence, and indicate whether changes were made.

Suggested attribution:

> Technology Commons teaching materials by Andrew Andrade, licensed under CC BY 4.0. Source: https://github.com/mrandrewandrade/assets

For an adaptation:

> Adapted from Technology Commons teaching materials by Andrew Andrade, licensed under CC BY 4.0. Changes were made. Source: https://github.com/mrandrewandrade/assets

See [LICENSE.md](LICENSE.md) for the licence notice and canonical licence link.
