#!/usr/bin/env bash
set -e

case "${1:-}" in
  about-me)
    mkdir -p dist

    quarto render assignments/about-me-presentation.qmd
    mv -f assignments/about-me-presentation.pdf dist/about-me-presentation.pdf

    quarto typst compile assignments/about-me-audience-notes.typ assignments/about-me-audience-notes.pdf
    mv -f assignments/about-me-audience-notes.pdf dist/about-me-audience-notes.pdf

    quarto typst compile assignments/about-me-teacher-marking.typ assignments/about-me-teacher-marking.pdf
    mv -f assignments/about-me-teacher-marking.pdf dist/about-me-teacher-marking.pdf
    ;;
  *)
    echo "Use: bash render.sh about-me"
    exit 1
    ;;
esac
