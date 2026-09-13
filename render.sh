#!/usr/bin/env bash
set -e

mkdir -p dist

build_presentation() {
  quarto render assignments/about-me-presentation.qmd
  mv -f assignments/about-me-presentation.pdf dist/about-me-presentation.pdf

  quarto render assignments/about-me-presentation-word.qmd
  mv -f assignments/about-me-presentation.docx dist/about-me-presentation.docx

  quarto render assignments/about-me-teacher-marking.qmd
  mv -f assignments/about-me-teacher-marking.pdf dist/about-me-presentation-teacher-marking.pdf
}

build_listening() {
  quarto render assignments/about-me-listening.qmd
  mv -f assignments/about-me-listening.pdf dist/about-me-listening.pdf

  quarto render assignments/about-me-listening-word.qmd
  mv -f assignments/about-me-listening.docx dist/about-me-listening.docx

  quarto render assignments/about-me-listening-notes.qmd
  mv -f assignments/about-me-listening-notes.pdf dist/about-me-listening-notes.pdf

  quarto render assignments/about-me-listening-teacher-marking.qmd
  mv -f assignments/about-me-listening-teacher-marking.pdf dist/about-me-listening-teacher-marking.pdf
}

case "${1:-}" in
  about-me|about-me-all)
    build_presentation
    build_listening
    ;;
  about-me-presentation)
    build_presentation
    ;;
  about-me-listening)
    build_listening
    ;;
  *)
    echo "Use:"
    echo "  bash render.sh about-me"
    echo "  bash render.sh about-me-presentation"
    echo "  bash render.sh about-me-listening"
    exit 1
    ;;
esac
