#!/usr/bin/env bash
set -e

mkdir -p dist

build_presentation() {
  quarto render assignments/about-me-presentation.qmd
  mv -f assignments/about-me-presentation.pdf dist/past-present-becoming.pdf

  quarto render assignments/about-me-presentation-word.qmd
  mv -f assignments/past-present-becoming.docx dist/past-present-becoming.docx

  quarto render assignments/about-me-teacher-marking.qmd
  mv -f assignments/about-me-teacher-marking.pdf dist/past-present-becoming-teacher-marking.pdf
}

build_listening() {
  quarto render assignments/about-me-listening.qmd
  mv -f assignments/about-me-listening.pdf dist/the-way-we-meet.pdf

  quarto render assignments/about-me-listening-word.qmd
  mv -f assignments/the-way-we-meet.docx dist/the-way-we-meet.docx

  quarto render assignments/about-me-listening-notes.qmd
  mv -f assignments/about-me-listening-notes.pdf dist/the-way-we-meet-notes.pdf

  quarto render assignments/about-me-listening-teacher-marking.qmd
  mv -f assignments/about-me-listening-teacher-marking.pdf dist/the-way-we-meet-teacher-marking.pdf
}

case "${1:-}" in
  about-me|about-me-all)
    build_presentation
    build_listening
    ;;
  past-present-becoming|about-me-presentation)
    build_presentation
    ;;
  the-way-we-meet|about-me-listening)
    build_listening
    ;;
  *)
    echo "Use:"
    echo "  bash render.sh about-me"
    echo "  bash render.sh past-present-becoming"
    echo "  bash render.sh the-way-we-meet"
    exit 1
    ;;
esac
