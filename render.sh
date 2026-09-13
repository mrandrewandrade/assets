#!/usr/bin/env bash
set -e

mkdir -p dist

# Remove superseded separate teacher trackers from older local builds.
rm -f \
  dist/past-present-becoming-teacher-marking.pdf \
  dist/past-present-becoming-teacher-marking.docx \
  dist/the-way-we-meet-teacher-marking.pdf \
  dist/the-way-we-meet-teacher-marking.docx

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

  quarto pandoc assignments/combined-teacher-marking-word.md --to docx --output assignments/combined-teacher-marking.docx
  mv -f assignments/combined-teacher-marking.docx dist/combined-teacher-marking.docx
}

case "${1:-}" in
  about-me|about-me-all)
    build_presentation
    build_listening
    build_teacher_marking
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
    echo "  bash render.sh past-present-becoming"
    echo "  bash render.sh the-way-we-meet"
    echo "  bash render.sh combined-teacher-marking"
    exit 1
    ;;
esac
