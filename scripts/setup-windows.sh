#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v quarto >/dev/null 2>&1; then
  echo "Quarto is required to build the PDFs locally."
  echo
  echo "On Windows, install it with:"
  echo "  winget install --id Posit.Quarto -e"
  echo
  echo "Then close and reopen Git Bash and run this script again."
  exit 1
fi

echo "Quarto:"
quarto --version

echo
echo_typst() {
  echo "Typst bundled with Quarto:"
  quarto typst --version
}
echo_typst

echo
quarto check

echo
echo "Local PDF toolchain is ready."
echo "Build the About Me PDF with:"
echo "  bash render.sh about-me"
echo
echo "Output:"
echo "  dist/about-me-presentation.pdf"
