#!/usr/bin/env bash
# Connect linkedin-ads MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="linkedin-ads"
if mcp_exists "linkedin-ads"; then
  green "linkedin-ads MCP already configured"
  exit 0
fi
TOK_FILE="$HOME/.marketing-agency/tokens/linkedin.json"
if [ ! -f "$TOK_FILE" ]; then
  yellow "linkedin-ads needs Phase 3 LinkedIn onboarding first"
  exit 0
fi
TOKEN=$(jq -r '.access_token // empty' "$TOK_FILE")
if [ -z "$TOKEN" ]; then
  yellow "linkedin-ads access_token missing — Marketing API still pending approval?"
  exit 0
fi
mcp_add_uvx "linkedin-ads" "linkedin-ads-mcp" "--access-token" "$TOKEN"
green "linkedin-ads MCP added"
