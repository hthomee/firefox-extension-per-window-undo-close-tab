#!/usr/bin/env bash
# Renders the PNG icons (transparent background) from extension/icons/icon.svg with resvg.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/make-icon.py
for size in 48 96 128; do
  npx --yes @resvg/resvg-js-cli --fit-width "$size" extension/icons/icon.svg "extension/icons/icon-${size}.png"
done
