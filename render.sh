#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

export TYPST_FONT_PATHS="${PWD}/brand/fonts${TYPST_FONT_PATHS:+:${TYPST_FONT_PATHS}}"

mkdir -p dist

# Remove old filenames from previous local builds so dist only shows the current names.
rm -f \
  dist/name-tag-pdf.pdf \
  dist/name-tag-pdf.docx \
  dist/past-present-becoming.pdf \
  dist/past-present-becoming.docx \
  dist/the-way-we-meet.pdf \
  dist/the-way-we-meet.docx \
  dist/the-way-we-meet-notes.pdf \
  dist/the-way-we-meet-notes-bw.pdf \
  dist/the-way-we-meet-notes.docx \
  dist/combined-teacher-marking.pdf \
  dist/combined-teacher-marking.docx \
  dist/past-present-becoming-teacher-marking.pdf \
  dist/past-present-becoming-teacher-marking.docx \
  dist/the-way-we-meet-teacher-marking.pdf \
  dist/the-way-we-meet-teacher-marking.docx \
  dist/about-me-audience-notes.pdf \
  dist/about-me-presentation.pdf \
  dist/about-me-teacher-marking.pdf \
  dist/weekly-smart-goal-progress-log.pdf \
  dist/weekly-smart-goal-progress-log-bw.pdf \
  dist/weekly-smart-goal-progress-log.docx

build_name_tag() {
  quarto render assignments/name-tag-pdf.qmd
  mv -f assignments/name-tag-pdf.pdf dist/0.0-name-tag-pdf.pdf

  quarto render assignments/name-tag-pdf-word.qmd
  mv -f assignments/name-tag-pdf.docx dist/0.0-name-tag-pdf.docx
}

build_presentation() {
  quarto render assignments/about-me-presentation.qmd
  mv -f assignments/about-me-presentation.pdf dist/0.1-past-present-becoming.pdf

  quarto render assignments/about-me-presentation-word.qmd
  mv -f assignments/past-present-becoming.docx dist/0.1-past-present-becoming.docx
}

build_listening() {
  quarto render assignments/about-me-listening.qmd
  mv -f assignments/about-me-listening.pdf dist/0.2-the-way-we-meet.pdf

  quarto render assignments/about-me-listening-word.qmd
  mv -f assignments/the-way-we-meet.docx dist/0.2-the-way-we-meet.docx

  quarto render assignments/about-me-listening-notes.qmd
  mv -f assignments/about-me-listening-notes.pdf dist/0.2-the-way-we-meet-notes.pdf

  quarto render assignments/about-me-listening-notes-bw.qmd
  mv -f assignments/about-me-listening-notes-bw.pdf dist/0.2-the-way-we-meet-notes-bw.pdf

  quarto render assignments/about-me-listening-notes-word.qmd
  mv -f assignments/the-way-we-meet-notes.docx dist/0.2-the-way-we-meet-notes.docx
}

build_teacher_marking() {
  quarto render assignments/combined-teacher-marking.qmd
  mv -f assignments/combined-teacher-marking.pdf dist/0.1-0.2-combined-teacher-marking.pdf

  quarto render assignments/combined-teacher-marking-word.qmd
  mv -f assignments/combined-teacher-marking.docx dist/0.1-0.2-combined-teacher-marking.docx
}

build_weekly_progress() {
  quarto render assignments/weekly-smart-goal-progress-log.qmd
  mv -f assignments/weekly-smart-goal-progress-log.pdf dist/weekly-smart-goal-progress-log.pdf

  quarto render assignments/weekly-smart-goal-progress-log-bw.qmd
  mv -f assignments/weekly-smart-goal-progress-log-bw.pdf dist/weekly-smart-goal-progress-log-bw.pdf

  quarto render assignments/weekly-smart-goal-progress-log-word.qmd
  mv -f assignments/weekly-smart-goal-progress-log.docx dist/weekly-smart-goal-progress-log.docx
}

case "${1:-}" in
  about-me|about-me-all|0-series|all)
    build_name_tag
    build_presentation
    build_listening
    build_teacher_marking
    build_weekly_progress
    ;;
  0.0|0.0-name-tag|name-tag|name-tag-pdf)
    build_name_tag
    ;;
  0.1|0.1-past-present-becoming|past-present-becoming|about-me-presentation)
    build_presentation
    ;;
  0.2|0.2-the-way-we-meet|the-way-we-meet|about-me-listening)
    build_listening
    ;;
  combined-teacher-marking|0.1-0.2-combined-teacher-marking)
    build_teacher_marking
    ;;
  weekly|weekly-smart|weekly-progress|progress-log|weekly-smart-goal-progress-log|weekly-smart-goal-progress-log-bw)
    build_weekly_progress
    ;;
  *)
    echo "Use:"
    echo "  bash render.sh all"
    echo "  bash render.sh about-me"
    echo "  bash render.sh 0.0"
    echo "  bash render.sh 0.1"
    echo "  bash render.sh 0.2"
    echo "  bash render.sh combined-teacher-marking"
    echo "  bash render.sh weekly"
    exit 1
    ;;
esac
