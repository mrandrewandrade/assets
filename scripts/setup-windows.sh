#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if ! command -v quarto >/dev/null 2>&1; then
  echo "Quarto is required to build the teaching resources locally."
  echo
  echo "On Windows, install it with:"
  echo "  winget install --id Posit.Quarto -e"
  echo
  echo "Then close and reopen Git Bash and run this script again."
  exit 1
fi

if command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD="python"
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD="py -3"
else
  echo "Python 3 is required to generate the editable combined teacher marking DOCX."
  echo
  echo "On Windows, install Python 3 with:"
  echo "  winget install --id Python.Python.3.13 -e"
  echo
  echo "Then close and reopen Git Bash and run this script again."
  exit 1
fi

echo "Quarto:"
quarto --version

echo
echo "Typst bundled with Quarto:"
quarto typst --version

echo
echo "Python:"
$PYTHON_CMD --version

echo
quarto check

echo
echo "Local teaching-resource toolchain is ready."
echo "Build the complete package with:"
echo "  bash render.sh about-me"
echo
echo "Outputs are written to:"
echo "  dist/"
