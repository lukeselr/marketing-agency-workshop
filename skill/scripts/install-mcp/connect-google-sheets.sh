#!/usr/bin/env bash
# Connect google-sheets MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="google-sheets"
if mcp_exists "google-sheets"; then
  green "google-sheets MCP already configured"
  exit 0
fi
yellow "google-sheets: covered by 'google-drive' connector + 'googlesheets-automation' skill. No separate MCP needed."
