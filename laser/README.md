# Technology Commons Laser Fabrication Library

This directory is the source of truth for the Technology Commons laser-cutting catalogue. The library is generated from reviewed configuration and reusable geometry functions; generated SVGs are not hand-maintained.

## Student workflow

1. Measure the actual sheet thickness with calipers.
2. Cut the calibration set for the exact material and machine.
3. Select a loose, slip, snug, or press-fit result.
4. Regenerate or edit the SVG in Inkscape with the measured values.
5. Verify document units, physical dimensions, layers/operations, and duplicate lines.
6. Cut a small sample, evaluate it, and iterate before a production run.

Nominal 1/4 inch plywood is **not assumed to be 6.35 mm**. The default configuration uses a clearly labelled 6.00 mm example value and every fit-sensitive record remains `unverified` until a physical test is recorded.

## Generate and validate

```sh
python laser/scripts/generate_library.py
python laser/scripts/validate_library.py
python -m unittest discover -s laser/tests -p "test_*.py" -v
```

Generation is deterministic. It writes canonical fabrication SVGs, colour-coded SVG previews, JSON/CSV manifests, checksums, and a ZIP download bundle under `laser/generated/`.

The `shop_coverage` lists in configuration are a design backlog. They are not
automatically turned into renamed generic plates. A holder is published only
after its retention geometry and parameters are purposefully defined.

## Operation convention

- `CUT`: red hairline (`#ff0000`), closed geometry where appropriate.
- `SCORE`: blue hairline (`#0000ff`).
- `ENGRAVE`: black (`#000000`).

Colour is a communication convention, not a machine setting. Confirm the local laser software's mapping before sending a job.

## Editing

Inkscape is the primary editor. Import at 100%, keep display units and document units in millimetres, and use **Object > Fill and Stroke** plus **Document Properties** to verify operations and size. The SVGs use simple primitives and paths, a millimetre canvas, a matching `viewBox`, no transforms, no embedded raster data, and no external fonts or resources.

Veccy is a browser-based parametric learning option. The curated recipes in `veccy/recipes.json` describe variables and graph-building steps for high-value designs. Veccy currently exposes variables and expression-driven feature parameters in its browser UI; the recipes are intentionally portable instructions rather than an undocumented private project-file format. Export the result to SVG, then verify it in Inkscape before fabrication.

## Repository map

```text
config/library.yml          reviewed families and default shop parameters
config/metadata.schema.json machine-readable metadata contract
scripts/                    generator and validator
tests/                      dimensional and metadata regression tests
veccy/recipes.json          curated parametric build recipes
docs/                       physical-test plan and design guidance
generated/svg/              canonical fabrication files
generated/previews/         web previews, not fabrication inputs
generated/catalog.json      complete machine-readable manifest
generated/catalog.csv       flat inventory export
generated/downloads/        deterministic bundle
```

## Verification states

`unverified`, `dimension-tested`, `fit-tested`, and `shop-tested` are the only accepted values. Generated files start as `unverified`; software validation does not imply physical verification.

## Licensing and provenance

Original procedural geometry and educational material are CC BY-SA 4.0, matching the repository licence. Generator and validator code are provided under the same repository licence unless a file states otherwise. The first catalogue contains only original procedural geometry; no paid artwork, protected team marks, branded tool silhouettes, or restricted cultural designs are copied or traced. See `provenance.yml`.
