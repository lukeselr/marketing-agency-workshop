#!/usr/bin/env bash
# Connect google-drive MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="google-drive"
if mcp_exists "google-drive"; then
  green "google-drive MCP already configured"
  exit 0
fi
yellow "google-drive MCP: enable via Claude Desktop → Settings → Connectors → Google Drive."
