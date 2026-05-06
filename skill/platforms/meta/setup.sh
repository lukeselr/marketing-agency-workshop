#!/usr/bin/env bash
# Meta platform onboarding orchestrator. Runs all 7 specs serially via Playwright MCP.
#
# Usage:
#   bash ~/.claude/skills/marketing-agency/platforms/meta/setup.sh
#
# Resumable: reads .state/meta-progress.json, skips already-completed steps.

set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
PLATFORM_DIR="$SKILL_DIR/platforms/meta"
STATE_DIR="$SKILL_DIR/.state"
TOKENS_DIR="$HOME/.marketing-agency/tokens"
PROGRESS="$STATE_DIR/meta-progress.json"

mkdir -p "$STATE_DIR" "$TOKENS_DIR"
chmod 700 "$TOKENS_DIR"

[ -f "$PROGRESS" ] || echo '{"steps":{}}' > "$PROGRESS"

run_spec() {
  local step="$1"
  local file="$2"
  if jq -e ".steps[\"$step\"] == \"ok\"" "$PROGRESS" > /dev/null 2>&1; then
    echo "[skip] $step (already complete)"
    return 0
  fi
  echo "[run] $step"
  if npx playwright test "$file" --reporter=line; then
    jq ".steps[\"$step\"] = \"ok\"" "$PROGRESS" > "$PROGRESS.tmp" && mv "$PROGRESS.tmp" "$PROGRESS"
    echo "[ok] $step"
  else
    echo "[fail] $step — see logs. Resume by re-running this script."
    exit 1
  fi
}

cd "$PLATFORM_DIR"
run_spec "00-create-or-signin" "playwright/00-create-or-signin.spec.ts"
run_spec "01-business-manager" "playwright/01-business-manager.spec.ts"
run_spec "02-ad-account" "playwright/02-ad-account.spec.ts"
run_spec "03-system-user" "playwright/03-system-user.spec.ts"
run_spec "04-pixel" "playwright/04-pixel.spec.ts"
run_spec "05-capi-dataset" "playwright/05-capi-dataset.spec.ts"
run_spec "06-leadgen-form" "playwright/06-leadgen-form.spec.ts"

echo "Meta onboarding complete. Token + IDs at $TOKENS_DIR/meta.json"
