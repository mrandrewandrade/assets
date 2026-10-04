#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p dist

if ! command -v magick >/dev/null 2>&1; then
  echo "ImageMagick is required to create print-ready schematic PDFs." >&2
  exit 1
fi
if ! command -v pdflatex >/dev/null 2>&1; then
  echo "pdfLaTeX is required to generate CircuitikZ schematics." >&2
  exit 1
fi
if ! command -v dvisvgm >/dev/null 2>&1; then
  echo "dvisvgm is required to generate vector SVG schematics." >&2
  exit 1
fi

schematic_build=tmp/schematics
mkdir -p "$schematic_build"
for source in electronics/schematics/*.tex; do
  base_name="$(basename "${source%.tex}")"
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$schematic_build" "$source" >/dev/null
  cp "$schematic_build/$base_name.pdf" "electronics/schematics/$base_name.pdf"
  dvisvgm --pdf --no-fonts --exact-bbox --bbox=min \
    --output="electronics/schematics/$base_name.svg" "$schematic_build/$base_name.pdf"
done

for schematic in electronics/schematics/*.svg; do
  if [[ -f "${schematic%.svg}.tex" ]]; then
    continue
  fi
  magick -density 144 "$schematic" -background white -alpha remove -alpha off -compress Zip "${schematic%.svg}.pdf"
done

render_pdf() {
  local source="$1"
  local output="$2"
  quarto render "$source" --to pdf --output "$output"
  mv -f "$output" "dist/$output"
}

render_pdf electronics/reference/TEJ-Electronics-Formula-Reference.qmd TEJ-Electronics-Formula-Reference.pdf
(
  cd electronics/reference
  quarto render TEJ-Electronics-Formula-Reference.qmd --to html --output TEJ-Electronics-Formula-Reference.html
)
mv -f electronics/reference/TEJ-Electronics-Formula-Reference.html dist/TEJ-Electronics-Formula-Reference.html

render_pdf electronics/worksheets/TEJ-Basic-Circuit-Calculations-Student-Worksheet.qmd TEJ_Basic_Circuit_Calculations_Student_Worksheet.pdf
render_pdf electronics/worksheets/TEJ-Basic-Circuit-Calculations-Answer-Key.qmd TEJ_Basic_Circuit_Calculations_Answer_Key.pdf

module_dir=electronics/modules/H01-safety-lab-practice
render_pdf "$module_dir/H01_Safety_Lab_Practice_Student_Worksheet.qmd" H01_Safety_Lab_Practice_Student_Worksheet.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Answer_Key.qmd" H01_Safety_Lab_Practice_Answer_Key.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Lab.qmd" H01_Safety_Lab_Practice_Lab.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Tinkercad_Guide.qmd" H01_Safety_Lab_Practice_Tinkercad_Guide.pdf

cp electronics/schematics/*.svg dist/
cp electronics/schematics/*.pdf dist/

echo "Rendered TEJ electronics assets to dist/."
