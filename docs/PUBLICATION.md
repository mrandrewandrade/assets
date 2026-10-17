# Public resource policy

This repository publishes blank teaching resources that are useful to students,
families, and educators. Public files must be intentionally selected. A file is
not publishable merely because it exists in the working directory.

## Public by default after review

- Original student assignments and handouts released under CC BY-SA 4.0.
- Blank planning, reflection, and Learning Skills tools.
- Current course outlines intended for students and families.
- Blank fillable classroom forms with no student information.
- Teacher assessment tools that do not contain student data or answer keys.
- Source files and brand assets required to rebuild the published resources.

## Keep out of the public repository

- Student work, names, numbers, signatures, contact information, or records.
- School inspection reports, room plans, inventories, and security-sensitive
  details.
- Answer keys and solution sets unless they are deliberately released for
  teacher use.
- Copyrighted video clips, downloaded media, and third-party documents that are
  not licensed for redistribution.
- Manufacturer manuals, OCTE packages, CCOHS downloads, and government source
  documents. Link to the authoritative publisher instead of republishing them.
- QA renders, temporary conversions, extracted document internals, caches, and
  local automation artifacts.
- Drafts that still contain placeholders, broken links, formatting defects, or
  machine-specific claims that have not been checked.

## Public site structure

- `assignments/` contains editable Quarto and Typst source.
- `dist/` contains generated PDFs and is rebuilt by GitHub Actions.
- `site/files/` contains reviewed prebuilt public PDFs, including fillable forms.
- `site/index.html` is the public catalogue.
- `electronics/` contains public student sources and generated reference files.
  Answer keys and teacher-only material are written to `private-dist/`.
- `laser/` contains original vector sources, generation scripts, tests, and the
  downloadable classroom fabrication library.
- `scripts/create_course_outline_fillables.py` and
  `scripts/create_personal_items_fillable.py` add and validate AcroForm fields
  after a clean source PDF has been exported into the documented `tmp/pdfs/`
  working location.

## Release checklist

1. Build all generated resources with `bash render.sh all`.
2. Confirm every site link resolves to a staged file.
3. Render new or changed PDFs and visually inspect every page.
4. For fillable PDFs, verify the field tree, field names, widgets, and appearance
   streams.
5. Confirm the public set contains no student data, answer keys, inspection
   reports, restricted source material, or copyrighted media.
6. Check the site at desktop and mobile widths.
7. Commit only the allow-listed source, site, and reviewed public files.
8. Push the release commit, wait for GitHub Pages deployment, and create a dated
   GitHub release from the same commit.
