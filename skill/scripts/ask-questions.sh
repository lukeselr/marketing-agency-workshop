#!/usr/bin/env bash
# Phase 1.4 — capture the 5 lean private answers and merge into .state/profile.json.
# Designed for interactive use (Claude Code session OR terminal).
set -u
STATE_DIR="$HOME/.claude/skills/marketing-agency/.state"
PROFILE="$STATE_DIR/profile.json"
mkdir -p "$STATE_DIR"
[ -f "$PROFILE" ] || echo '{}' > "$PROFILE"

# Allow non-interactive runs via env vars (great for the LLM driver):
#   MA_BUDGET_AUD MA_BOTTLENECK MA_REAL_COMPETITORS MA_COMFORT_META MA_COMFORT_GOOGLE MA_COMFORT_LINKEDIN MA_EXISTING_ACCOUNTS
ask() {
  local label="$1" envvar="$2" default="${3:-}"
  local val="${!envvar:-}"
  if [ -z "$val" ] && [ -t 0 ]; then
    printf "\n  %s\n  %s> " "$label" "$envvar"
    read -r val
  fi
  [ -n "$val" ] || val="$default"
  echo "$val"
}

budget=$(ask "1) Monthly ad budget (AUD, total across platforms)?" MA_BUDGET_AUD "")
bottleneck=$(ask "2) Most painful bottleneck in your business right now?" MA_BOTTLENECK "")
real_comp=$(ask "3) Of detected competitors, which 1-2 are the real threat?" MA_REAL_COMPETITORS "")
comfort_meta=$(ask "4a) Comfort 1-5 with Meta (FB/IG) Ads?" MA_COMFORT_META "1")
comfort_google=$(ask "4b) Comfort 1-5 with Google Ads?" MA_COMFORT_GOOGLE "1")
comfort_li=$(ask "4c) Comfort 1-5 with LinkedIn Ads?" MA_COMFORT_LINKEDIN "1")
existing=$(ask "5) Existing ad accounts to connect (Y/N)? If Y, paste account IDs (comma-sep, optional)." MA_EXISTING_ACCOUNTS "N")

jq \
  --arg budget "$budget" \
  --arg bottleneck "$bottleneck" \
  --arg real_comp "$real_comp" \
  --arg c_meta "$comfort_meta" \
  --arg c_google "$comfort_google" \
  --arg c_li "$comfort_li" \
  --arg existing "$existing" \
  '. + {
    "budget_aud_monthly": $budget,
    "bottleneck": $bottleneck,
    "real_competitors": $real_comp,
    "comfort": {"meta": $c_meta, "google": $c_google, "linkedin": $c_li},
    "existing_accounts": $existing,
    "captured_at": now | todate
  }' "$PROFILE" > "$PROFILE.tmp" && mv "$PROFILE.tmp" "$PROFILE"

echo
echo "Saved to $PROFILE"
jq . "$PROFILE"
