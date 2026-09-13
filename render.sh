#!/usr/bin/env bash
set -e

mkdir -p dist

# Remove superseded separate teacher trackers from older local builds.
rm -f \
  dist/past-present-becoming-teacher-marking.pdf \
  dist/past-present-becoming-teacher-marking.docx \
  dist/the-way-we-meet-teacher-marking.pdf \
  dist/the-way-we-meet-teacher-marking.docx

run_python_script() {
  if command -v python3 >/dev/null 2>&1; then
    python3 "$@"
  elif command -v python >/dev/null 2>&1; then
    python "$@"
  elif command -v py >/dev/null 2>&1; then
    py -3 "$@"
  else
    echo "Python 3 is required to generate the editable combined teacher marking DOCX."
    echo "Install Python 3, reopen Git Bash, and run this command again."
    exit 1
  fi
}

build_name_tag() {
  quarto render assignments/name-tag-pdf.qmd
  mv -f assignments/name-tag-pdf.pdf dist/name-tag-pdf.pdf

  quarto render assignments/name-tag-pdf-word.qmd
  mv -f assignments/name-tag-pdf.docx dist/name-tag-pdf.docx
}

build_presentation() {
  quarto render assignments/about-me-presentation.qmd
  mv -f assignments/about-me-presentation.pdf dist/past-present-becoming.pdf

  quarto render assignments/about-me-presentation-word.qmd
  mv -f assignments/past-present-becoming.docx dist/past-present-becoming.docx
}

build_listening() {
  quarto render assignments/about-me-listening.qmd
  mv -f assignments/about-me-listening.pdf dist/the-way-we-meet.pdf

  quarto render assignments/about-me-listening-word.qmd
  mv -f assignments/the-way-we-meet.docx dist/the-way-we-meet.docx

  quarto render assignments/about-me-listening-notes.qmd
  mv -f assignments/about-me-listening-notes.pdf dist/the-way-we-meet-notes.pdf

  quarto render assignments/about-me-listening-notes-word.qmd
  mv -f assignments/the-way-we-meet-notes.docx dist/the-way-we-meet-notes.docx
}

build_teacher_marking() {
  quarto render assignments/combined-teacher-marking.qmd
  mv -f assignments/combined-teacher-marking.pdf dist/combined-teacher-marking.pdf

  run_python_script scripts/build_combined_teacher_word.py
  mv -f assignments/combined-teacher-marking.docx dist/combined-teacher-marking.docx
}

case "${1:-}" in
  about-me|about-me-all)
    build_name_tag
    build_presentation
    build_listening
    build_teacher_marking
    ;;
  name-tag|name-tag-pdf)
    build_name_tag
    ;;
  past-present-becoming|about-me-presentation)
    build_presentation
    ;;
  the-way-we-meet|about-me-listening)
    build_listening
    ;;
  combined-teacher-marking)
    build_teacher_marking
    ;;
  *)
    echo "Use:"
    echo "  bash render.sh about-me"
    echo "  bash render.sh name-tag-pdf"
    echo "  bash render.sh past-present-becoming"
    echo "  bash render.sh the-way-we-meet"
    echo "  bash render.sh combined-teacher-marking"
    exit 1
    ;;
esac
