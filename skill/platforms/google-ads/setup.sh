#!/usr/bin/env bash
# Google Ads platform onboarding orchestrator.
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
PLATFORM_DIR="$SKILL_DIR/platforms/google-ads"
STATE_DIR="$SKILL_DIR/.state"
TOKENS_DIR="$HOME/.marketing-agency/tokens"
PROGRESS="$STATE_DIR/google-ads-progress.json"

mkdir -p "$STATE_DIR" "$TOKENS_DIR"
chmod 700 "$TOKENS_DIR"

if [ -f "$SKILL_DIR/.env" ]; then
  set -a; . "$SKILL_DIR/.env"; set +a
fi

[ -f "$PROGRESS" ] || echo '{"steps":{}}' > "$PROGRESS"

run_spec() {
  local step="$1" file="$2"
  if jq -e ".steps[\"$step\"] == \"ok\"" "$PROGRESS" > /dev/null 2>&1; then
    echo "[skip] $step"
    return 0
  fi
  echo "[run] $step"
  if npx playwright test "$file" --reporter=line; then
    jq ".steps[\"$step\"] = \"ok\"" "$PROGRESS" > "$PROGRESS.tmp" && mv "$PROGRESS.tmp" "$PROGRESS"
    echo "[ok] $step"
  else
    echo "[fail] $step — resume by re-running this script."
    exit 1
  fi
}

cd "$PLATFORM_DIR"
run_spec "00-create-or-signin" "playwright/00-create-or-signin.spec.ts"
run_spec "01-cloud-project" "playwright/01-cloud-project.spec.ts"
run_spec "02-mcc-account" "playwright/02-mcc-account.spec.ts"
run_spec "03-developer-token" "playwright/03-developer-token.spec.ts"
run_spec "04-oauth-credentials" "playwright/04-oauth-credentials.spec.ts"
run_spec "05-conversion-tracking" "playwright/05-conversion-tracking.spec.ts"
run_spec "06-search-campaign" "playwright/06-search-campaign.spec.ts"
echo "Google Ads onboarding complete. Token + IDs at $TOKENS_DIR/google-ads.json"
