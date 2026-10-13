#!/usr/bin/env bash
# Builds dist/per-window-undo-close-tab-<version>.zip from the extension/ folder.
# There is no build step for the code itself: the zip contains the files exactly as they are in the repository.
set -euo pipefail
cd "$(dirname "$0")/.."

version="$(python3 -c 'import json; print(json.load(open("extension/manifest.json"))["version"])')"
mkdir -p dist
out="dist/per-window-undo-close-tab-${version}.zip"
rm -f "$out"
(cd extension && zip -q -r -X "../${out}" . -x '.DS_Store' -x '*/.DS_Store')
echo "$out"
