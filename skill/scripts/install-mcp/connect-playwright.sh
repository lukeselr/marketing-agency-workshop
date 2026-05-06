#!/usr/bin/env bash
# Connect playwright MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="playwright"
if mcp_exists "playwright"; then
  green "playwright MCP already configured"
  exit 0
fi
mcp_add_npx "playwright" "@anthropic-ai/playwright-mcp"
green "playwright MCP added (restart Claude Code to activate)"
