#!/usr/bin/env bash
set -euo pipefail

# Simple helper to build a single-file executable with pyinstaller
# Usage: ./build.sh

if ! command -v pyinstaller >/dev/null 2>&1; then
  echo "pyinstaller not found. Install with: pip install pyinstaller"
  exit 1
fi

MAIN=virtual_ai_gui.py
OUT=dist

echo "Building ${MAIN} with pyinstaller..."
pyinstaller --onefile --windowed --name virtual-ai-desktop "${MAIN}"

echo "Build complete. Find executable in ./dist/" 