#!/usr/bin/env bash
# Connect meta-ads MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="meta-ads"
if mcp_exists "meta-ads"; then
  green "meta-ads MCP already configured"
  exit 0
fi
TOK_FILE="$HOME/.marketing-agency/tokens/meta.json"
if [ ! -f "$TOK_FILE" ]; then
  yellow "meta-ads needs Phase 3 Meta onboarding first (no token yet). Run: bash platforms/meta/setup.sh"
  exit 0
fi
TOKEN=$(jq -r '.system_user_token // empty' "$TOK_FILE")
AD_ID=$(jq -r '.ad_account_id // empty' "$TOK_FILE")
if [ -z "$TOKEN" ] || [ -z "$AD_ID" ]; then
  red "meta-ads tokens incomplete in $TOK_FILE"
  exit 1
fi
mcp_add_uvx "meta-ads" "meta-ads-mcp" "--access-token" "$TOKEN" "--ad-account-id" "$AD_ID"
green "meta-ads MCP added"
