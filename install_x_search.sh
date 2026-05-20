#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if uv tool list | grep -q '^x-search-cli '; then
  uv tool install --editable --reinstall "$SCRIPT_DIR"
else
  uv tool install --editable "$SCRIPT_DIR"
fi
