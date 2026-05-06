#!/usr/bin/env bash
# Connect slack MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="slack"
if mcp_exists "slack"; then
  green "slack MCP already configured"
  exit 0
fi
yellow "slack: optional. Claude Desktop has Slack connector. Enable for hot-lead alerts."
