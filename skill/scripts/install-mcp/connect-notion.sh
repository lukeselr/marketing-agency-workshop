#!/usr/bin/env bash
# Connect notion MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="notion"
if mcp_exists "notion"; then
  green "notion MCP already configured"
  exit 0
fi
yellow "notion: Claude Desktop has Notion connector. Enable in Settings → Connectors → Notion. Required for: weekly reports → Notion page, content calendar DB, monthly strategy deck."
