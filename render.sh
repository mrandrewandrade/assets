#!/usr/bin/env bash
set -e

case "${1:-}" in
  about-me)
    quarto render assignments/about-me-presentation.qmd
    mkdir -p dist
    mv -f assignments/about-me-presentation.pdf dist/about-me-presentation.pdf
    ;;
  *)
    echo "Use: bash render.sh about-me"
    exit 1
    ;;
esac
