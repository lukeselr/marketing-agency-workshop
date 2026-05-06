#!/usr/bin/env bash
# Phase 0 pre-flight for marketing-agency.
# Auto-installs missing Python deps. No user-specific path checks; works on any machine.

set -u
PASS=0
FAIL=0
WARN=0
BLOCKERS=""

note() { printf "  %s  %s\n" "$1" "$2"; }
ok()    { note "✓" "$1"; PASS=$((PASS+1)); }
bad()   { note "✗" "$1"; FAIL=$((FAIL+1)); BLOCKERS="${BLOCKERS}\n  - $1"; }
warn()  { note "!" "$1 (non-blocking)"; WARN=$((WARN+1)); }

check() {
  local label="$1" cmd="$2" critical="${3:-yes}"
  if eval "$cmd" >/dev/null 2>&1; then
    ok "$label"
  elif [ "$critical" = "yes" ]; then
    bad "$label"
  else
    warn "$label"
  fi
}

# Try to install missing pip deps quietly (--user, no sudo)
ensure_pip_dep() {
  local mod="$1" pip_name="${2:-$1}"
  if python3 -c "import $mod" >/dev/null 2>&1; then
    ok "Python: $mod"
    return 0
  fi
  if command -v pip3 >/dev/null 2>&1; then
    if pip3 install --user --quiet "$pip_name" >/dev/null 2>&1; then
      ok "Python: $mod (auto-installed)"
      return 0
    fi
  fi
  warn "Python: $mod (could not auto-install — \`pip3 install --user $pip_name\`)"
}

echo
echo "marketing-agency Phase 0 pre-flight"
echo "===================================="
echo
echo "Core toolchain:"
check "node 18+"   "node --version | sed 's/v//' | awk -F. '{exit (\$1 < 18)}'"
check "npm"        "command -v npm"
check "python 3.10+" "python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'"
check "git"        "command -v git"
check "jq"         "command -v jq"
check "curl"       "command -v curl"
check "gh CLI"     "command -v gh" "no"

echo
echo "Free scrape stack:"
check "dig (DNS)"  "command -v dig"
check "whois"      "command -v whois" "no"
ensure_pip_dep "requests"
ensure_pip_dep "bs4" "beautifulsoup4"

echo
echo "Claude Code config:"
mkdir -p "$HOME/.claude" && [ -f "$HOME/.claude.json" ] || echo '{"mcpServers": {}}' > "$HOME/.claude.json"
ok "~/.claude.json present"
mkdir -p "$HOME/.marketing-agency/tokens" && chmod 700 "$HOME/.marketing-agency" "$HOME/.marketing-agency/tokens"
ok "~/.marketing-agency/ runtime dir (mode 700)"

echo
echo "Optional MCPs (skill works fine without these — Phase 5 installs them):"
# `claude mcp list` can hang outside an active session. Skip if claude not on PATH or call times out.
mcp_safe() {
  command -v claude >/dev/null 2>&1 || return 1
  if command -v timeout >/dev/null 2>&1; then
    timeout 4 claude mcp list 2>/dev/null
  elif command -v gtimeout >/dev/null 2>&1; then
    gtimeout 4 claude mcp list 2>/dev/null
  else
    # No timeout available — skip the MCP probe entirely so we never hang.
    return 1
  fi
}
check "Playwright MCP" "mcp_safe | grep -qiE 'playwright.*Connected'" "no"
check "Meta Ads MCP" "mcp_safe | grep -qiE 'meta-ads.*Connected'" "no"
check "LinkedIn Ads MCP" "mcp_safe | grep -qiE 'linkedin-ads.*Connected'" "no"
check "Gmail MCP"   "mcp_safe | grep -qiE 'Gmail.*Connected'" "no"

echo
echo "===================================="
echo "Result: $PASS passed, $WARN warnings, $FAIL blockers"
echo

if [ "$FAIL" -gt 0 ]; then
  printf "Blockers to fix before continuing:%b\n\n" "$BLOCKERS"
  exit 1
fi

echo "Pre-flight green. Proceed to Phase 1 (auto-discovery)."
exit 0
