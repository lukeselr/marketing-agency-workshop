#!/usr/bin/env bash
# LinkedIn platform onboarding orchestrator.
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
PLATFORM_DIR="$SKILL_DIR/platforms/linkedin"
STATE_DIR="$SKILL_DIR/.state"
TOKENS_DIR="$HOME/.marketing-agency/tokens"
PROGRESS="$STATE_DIR/linkedin-progress.json"

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
run_spec "01-dev-app" "playwright/01-dev-app.spec.ts"
run_spec "02-marketing-api-request" "playwright/02-marketing-api-request.spec.ts"
echo "[wait] LinkedIn Marketing API approval is 1-5 business days. Run while-you-wait engagement loop."
echo "[wait] After approval email arrives, run:"
echo "       bash $0 --post-approval"

if [ "${1:-}" = "--post-approval" ]; then
  run_spec "03-oauth-tokens" "playwright/03-oauth-tokens.spec.ts"
  run_spec "04-insight-tag" "playwright/04-insight-tag.spec.ts"
  run_spec "05-leadgen-form" "playwright/05-leadgen-form.spec.ts"
  echo "LinkedIn onboarding complete."
fi
