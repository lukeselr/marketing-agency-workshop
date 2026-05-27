#!/usr/bin/env bash
# Shared library for MCP install scripts.
set -u
CC_CONFIG="${HOME}/.claude.json"
[ -f "$CC_CONFIG" ] || echo '{"mcpServers": {}}' > "$CC_CONFIG"

backup_cc_config() {
  # Snapshot ~/.claude.json before every mutation. Cheap insurance against
  # a malformed jq filter or a half-written file killing the user's whole
  # Claude Code config. Kept silent on failure (e.g. read-only FS during CI).
  cp "$CC_CONFIG" "$CC_CONFIG.bak.$(date +%s)" 2>/dev/null || true
}

mcp_exists() {
  local name="$1"
  jq -e --arg n "$name" '.mcpServers | has($n)' "$CC_CONFIG" > /dev/null 2>&1
}

mcp_add_npx() {
  local name="$1"; shift
  local pkg="$1"; shift
  local args_json
  args_json=$(printf '%s\n' "$@" | jq -R . | jq -s .)
  backup_cc_config
  jq --arg n "$name" --arg pkg "$pkg" --argjson a "$args_json" \
    '.mcpServers[$n] = {"command": "npx", "args": (["-y", $pkg] + $a)}' \
    "$CC_CONFIG" > "$CC_CONFIG.tmp" && mv "$CC_CONFIG.tmp" "$CC_CONFIG"
}

mcp_add_uvx() {
  local name="$1"; shift
  local pkg="$1"; shift
  local args_json
  args_json=$(printf '%s\n' "$@" | jq -R . | jq -s .)
  backup_cc_config
  jq --arg n "$name" --arg pkg "$pkg" --argjson a "$args_json" \
    '.mcpServers[$n] = {"command": "uvx", "args": ([$pkg] + $a)}' \
    "$CC_CONFIG" > "$CC_CONFIG.tmp" && mv "$CC_CONFIG.tmp" "$CC_CONFIG"
}

green() { printf "  \033[32m✓\033[0m  %s\n" "$1"; }
yellow() { printf "  \033[33m!\033[0m  %s\n" "$1"; }
red()    { printf "  \033[31m✗\033[0m  %s\n" "$1"; }
