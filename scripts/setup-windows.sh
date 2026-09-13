#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

if [ ! -f .venv/Scripts/python.exe ]; then
  py -3 -m venv .venv 2>/dev/null || python -m venv .venv
fi

.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m playwright install chromium
