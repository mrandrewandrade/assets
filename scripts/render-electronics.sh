#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."
mkdir -p dist

if command -v magick >/dev/null 2>&1; then
  imagemagick=(magick)
elif command -v convert >/dev/null 2>&1; then
  imagemagick=(convert)
else
  imagemagick=()
  echo "ImageMagick is unavailable; using committed PDFs for SVG-only schematics."
fi
regenerate_schematics=true
if ! command -v pdflatex >/dev/null 2>&1 || ! command -v dvisvgm >/dev/null 2>&1; then
  regenerate_schematics=false
  echo "CircuitikZ conversion tools are incomplete; using committed schematic PDFs and SVGs."
fi

schematic_build=tmp/schematics
mkdir -p "$schematic_build"
if [[ "$regenerate_schematics" == true ]]; then
  for source in electronics/schematics/*.tex; do
    base_name="$(basename "${source%.tex}")"
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory="$schematic_build" "$source" >/dev/null
    cp "$schematic_build/$base_name.pdf" "electronics/schematics/$base_name.pdf"
    dvisvgm --pdf --no-fonts --exact-bbox --bbox=min \
      --output="electronics/schematics/$base_name.svg" "$schematic_build/$base_name.pdf"
  done
fi

for schematic in electronics/schematics/*.svg; do
  if [[ -f "${schematic%.svg}.tex" ]]; then
    continue
  fi
  if (( ${#imagemagick[@]} )); then
    "${imagemagick[@]}" -density 144 "$schematic" -background white -alpha remove -alpha off -compress Zip "${schematic%.svg}.pdf"
  elif [[ ! -f "${schematic%.svg}.pdf" ]]; then
    echo "Missing committed PDF fallback for $schematic." >&2
    exit 1
  fi
done

render_pdf() {
  local source="$1"
  local output="$2"
  quarto render "$source" --to pdf --output "$output"
  mv -f "$output" "dist/$output"
}

render_pdf electronics/reference/TEJ-Electronics-Quick-Reference.qmd TEJ-Electronics-Quick-Reference.pdf
render_pdf electronics/reference/TEJ-Electronics-Reference-Handbook.qmd TEJ-Electronics-Reference-Handbook.pdf
(
  cd electronics/reference
  quarto render TEJ-Electronics-Reference-Handbook.qmd --to html --output TEJ-Electronics-Reference-Handbook.html
)
mv -f electronics/reference/TEJ-Electronics-Reference-Handbook.html dist/TEJ-Electronics-Reference-Handbook.html

render_pdf electronics/worksheets/TEJ-Basic-Circuit-Calculations-Student-Worksheet.qmd TEJ_Basic_Circuit_Calculations_Student_Worksheet.pdf
render_pdf electronics/worksheets/TEJ-Basic-Circuit-Calculations-Answer-Key.qmd TEJ_Basic_Circuit_Calculations_Answer_Key.pdf

module_dir=electronics/modules/H01-safety-lab-practice
render_pdf "$module_dir/H01_Safety_Lab_Practice_Student_Worksheet.qmd" H01_Safety_Lab_Practice_Student_Worksheet.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Answer_Key.qmd" H01_Safety_Lab_Practice_Answer_Key.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Lab.qmd" H01_Safety_Lab_Practice_Lab.pdf
render_pdf "$module_dir/H01_Safety_Lab_Practice_Tinkercad_Guide.qmd" H01_Safety_Lab_Practice_Tinkercad_Guide.pdf

digital_dir=electronics/modules/D01-digital-inputs
render_pdf "$digital_dir/D01_Digital_Inputs_Student_Worksheet.qmd" D01_Digital_Inputs_Student_Worksheet.pdf
render_pdf "$digital_dir/D01_Digital_Inputs_Answer_Key.qmd" D01_Digital_Inputs_Answer_Key.pdf

control_dir=electronics/modules/C06-control-systems
render_pdf "$control_dir/C06_Control_Methods_Comparison_Student.qmd" C06_Control_Methods_Comparison_Student.pdf
render_pdf "$control_dir/C06_Control_Methods_Comparison_Answer_Key.qmd" C06_Control_Methods_Comparison_Answer_Key.pdf

computer_systems_dir=electronics/computer-systems
render_pdf "$computer_systems_dir/TEJ-Basic-Computer-Systems-Student-Activity-Packages.qmd" TEJ-Basic-Computer-Systems-Student-Activity-Packages.pdf
render_pdf "$computer_systems_dir/TEJ-Basic-Computer-Systems-Teacher-Guide.qmd" TEJ-Basic-Computer-Systems-Teacher-Guide.pdf
render_pdf "$computer_systems_dir/TEJ-Computer-Recovery-Crew-Pilot-Job-Sheet.qmd" TEJ-Computer-Recovery-Crew-Pilot-Job-Sheet.pdf
render_pdf "$computer_systems_dir/TEJ-Computer-Recovery-Crew-Pilot-Teacher-Launch-Guide.qmd" TEJ-Computer-Recovery-Crew-Pilot-Teacher-Launch-Guide.pdf
render_pdf "$computer_systems_dir/TEJ-Make-It-Print-Side-Quest.qmd" TEJ-Make-It-Print-Side-Quest.pdf
render_pdf "$computer_systems_dir/TEJ-Computer-Power-and-Parts-Mission.qmd" TEJ-Computer-Power-and-Parts-Mission.pdf
render_pdf "$computer_systems_dir/TEJ-Computer-Power-and-Parts-Teacher-Guide.qmd" TEJ-Computer-Power-and-Parts-Teacher-Guide.pdf

cp electronics/schematics/*.svg dist/
cp electronics/schematics/*.pdf dist/

echo "Rendered TEJ electronics assets to dist/."
