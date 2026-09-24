# Assets

Reusable branded teaching documents and source assets for Andrew Andrade's Technology Commons materials.

The goal of this repository is to keep student-facing documents simple, accessible, reproducible, and easy to revise. Current assignment PDFs are authored as Quarto documents and rendered with Typst. Matching editable Word versions are generated with Quarto/Pandoc.

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
site/                 GitHub Pages source
```

## Windows setup

The current toolchain requires Quarto. Typst is bundled with Quarto, so Typst does not need to be installed separately. Python is not required for the current 0-series resource build.

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
quarto check
```

## Build the 0-series resources

From the repository root:

```bash
bash render.sh about-me
```

The generated files are written to `dist/`:

```text
0.0-name-tag-pdf.pdf
0.0-name-tag-pdf.docx
0.1-past-present-becoming.pdf
0.1-past-present-becoming.docx
0.2-the-way-we-meet.pdf
0.2-the-way-we-meet.docx
0.2-the-way-we-meet-notes.pdf
0.2-the-way-we-meet-notes-bw.pdf
0.2-the-way-we-meet-notes.docx
0.1-0.2-combined-teacher-marking.pdf
0.1-0.2-combined-teacher-marking.docx
weekly-smart-goal-progress-log.pdf
weekly-smart-goal-progress-log-bw.pdf
weekly-smart-goal-progress-log.docx
```

Individual builds are also available:

```bash
bash render.sh 0.0
bash render.sh 0.1
bash render.sh 0.2
bash render.sh combined-teacher-marking
bash render.sh weekly
```

The GitHub Actions workflow uses the same Quarto/Typst/Pandoc rendering path, uploads the generated files in `dist/` as a workflow artifact, and publishes the PDFs and Word files to GitHub Pages.

## Creating another assignment

Use the existing `.qmd` assignments as a starting point and keep reusable images or branding in the appropriate asset folder. Add a matching command to `render.sh` when the assignment is ready to become part of the standard build.

## Legacy renderer

The repository still contains some earlier Markdown, HTML/CSS, Python, and Playwright tooling retained for reference. The current 0-series resources and GitHub Actions build use Quarto, Typst, and Pandoc.

## Licensing

Unless a file says otherwise, original educational material in this repository is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0)**.

**Share, adapt, and pass it on.** You may copy, modify, remix, and redistribute the material. Modified and adapted versions remain under **CC BY-SA 4.0**, identify that changes were made, and preserve attribution to the original source:

- https://andrewandrade.ca
- https://github.com/mrandrewandrade

You can also add your own name, website, repository, and links when you adapt the work so later versions can credit your contribution too. **Sharing is caring.**

Suggested attribution:

> Technology Commons teaching materials by Andrew Andrade and contributors. Original source: https://andrewandrade.ca and https://github.com/mrandrewandrade. Licensed under CC BY-SA 4.0.

For an adaptation:

> Based on Technology Commons teaching materials by Andrew Andrade and contributors. Original source: https://andrewandrade.ca and https://github.com/mrandrewandrade. Licensed under CC BY-SA 4.0. Modified by [your name], [your link]. Changes were made.

See [LICENSE.md](LICENSE.md) for the licence notice and canonical licence link.
