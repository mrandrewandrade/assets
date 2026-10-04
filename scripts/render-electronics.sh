#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p dist

if ! command -v magick >/dev/null 2>&1; then
  echo "ImageMagick is required to create print-ready schematic PDFs." >&2
  exit 1
fi

for schematic in electronics/schematics/*.svg; do
  magick -background white -density 144 "$schematic" "${schematic%.svg}.pdf"
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

cp electronics/schematics/H01_Safety_Lab_Practice_Schematic.svg dist/H01_Safety_Lab_Practice_Schematic.svg
cp electronics/schematics/H01_Blade_Fuse_Cutaway.svg dist/H01_Blade_Fuse_Cutaway.svg
cp electronics/schematics/Circuit_Calculations_Parallel_Schematic.svg dist/Circuit_Calculations_Parallel_Schematic.svg
cp electronics/schematics/H01_Safety_Lab_Practice_Schematic.pdf dist/H01_Safety_Lab_Practice_Schematic.pdf
cp electronics/schematics/H01_Blade_Fuse_Cutaway.pdf dist/H01_Blade_Fuse_Cutaway.pdf
cp electronics/schematics/Circuit_Calculations_Parallel_Schematic.pdf dist/Circuit_Calculations_Parallel_Schematic.pdf

echo "Rendered TEJ electronics assets to dist/."
