#!/usr/bin/env bash
# Safe ~/.claude.json + per-platform .env merge using jq pattern from xero-mcp-setup.
# Never blindly overwrites — reads existing JSON, merges, writes atomically.
set -u
CC_CONFIG="$HOME/.claude.json"
[ -f "$CC_CONFIG" ] || echo '{}' > "$CC_CONFIG"

backup_cc_config() {
  cp "$CC_CONFIG" "$CC_CONFIG.bak.$(date +%s)" 2>/dev/null || true
}

# Usage: secrets-handler.sh add-mcp <name> <command> <arg1> [arg2 ...]
cmd="${1:-}"
shift || true
case "$cmd" in
  add-mcp)
    name="$1"; shift
    binary="$1"; shift
    args_json=$(printf '%s\n' "$@" | jq -R . | jq -s .)
    backup_cc_config
    jq --arg n "$name" --arg b "$binary" --argjson a "$args_json" \
      '.mcpServers[$n] = {"command": $b, "args": $a}' "$CC_CONFIG" > "$CC_CONFIG.tmp"
    mv "$CC_CONFIG.tmp" "$CC_CONFIG"
    echo "[ok] mcp: $name"
    ;;
  remove-mcp)
    name="$1"
    backup_cc_config
    jq --arg n "$name" 'del(.mcpServers[$n])' "$CC_CONFIG" > "$CC_CONFIG.tmp"
    mv "$CC_CONFIG.tmp" "$CC_CONFIG"
    echo "[ok] removed mcp: $name"
    ;;
  *)
    echo "Usage: secrets-handler.sh {add-mcp|remove-mcp} <args>"; exit 1 ;;
esac
