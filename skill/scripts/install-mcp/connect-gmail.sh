#!/usr/bin/env bash
# Connect gmail MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="gmail"
if mcp_exists "gmail"; then
  green "gmail MCP already configured"
  exit 0
fi
yellow "gmail MCP install: Claude Desktop has built-in Gmail connector. Confirm it's enabled in Claude Desktop → Settings → Connectors. No CLI install needed."
