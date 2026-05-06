#!/usr/bin/env bash
# Connect telegram MCP. Idempotent.
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
. "$DIR/_lib.sh"

NAME="telegram"
if mcp_exists "telegram"; then
  green "telegram MCP already configured"
  exit 0
fi
yellow "telegram: bot token + chat_id needed. See $HOME/.claude/skills/marketing-agency/scripts/kill-rule-monitor.py for env vars (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID). MCP not required for alerts; direct API call works."
