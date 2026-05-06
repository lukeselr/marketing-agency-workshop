#!/usr/bin/env bash
# marketing-agency state-aware driver.
# Reads .state/ to figure out where the user is, suggests next phase.
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
STATE="$SKILL_DIR/.state"
INPUT="${1:-}"

# First-run: no baseline yet → run Phase 0 + 1
if [ ! -f "$STATE/business-baseline.md" ]; then
  if [ -z "$INPUT" ]; then
    echo "Usage: bash run.sh <business_url_or_name>"
    echo "First-run mode: provide a URL or business name to start Phase 1 discovery."
    exit 1
  fi
  echo "==> Phase 0: pre-flight"
  bash "$SKILL_DIR/scripts/check-preflight.sh" || exit 1
  echo
  echo "==> Phase 1: auto-discovery"
  bash "$SKILL_DIR/scripts/discover.sh" "$INPUT"
  echo
  echo "==> Phase 1.5: voice fingerprint"
  python3 "$SKILL_DIR/scripts/voice-fingerprint.py"
  echo
  echo "==> Refreshing dashboard"
  bash "$SKILL_DIR/scripts/build-dashboard.sh"
  echo
  echo "✅ First-run complete."
  echo
  echo "Next:"
  echo "  cat $STATE/business-baseline.md       # review"
  echo "  bash $SKILL_DIR/scripts/ask-questions.sh   # capture 5 lean answers"
  echo "  Then in Claude Code: /marketing-agency to continue"
  exit 0
fi

# Already onboarded → present picker
echo "marketing-agency — current state"
echo "================================="
NAME=$(grep -E "^# Business Baseline" "$STATE/business-baseline.md" | head -1 | sed 's/# Business Baseline: //')
echo "Business: $NAME"
echo
echo "What would you like to do?"
echo "  1) Run weekly report (Phase 9.5)"
echo "  2) Refresh creative (Phase 7 — delegate-creative)"
echo "  3) Build/refresh landing page (Phase 6.5)"
echo "  4) Deploy lead lifecycle (Phase 10)"
echo "  5) Build content calendar (Phase 11)"
echo "  6) Run monthly strategy review (Phase 12)"
echo "  7) Re-run discovery (refresh baseline)"
echo "  8) Connect MCPs (idempotent)"
echo "  q) Quit"
echo
read -p "Choice [1-8/q]: " choice

case "$choice" in
  1) python3 "$SKILL_DIR/scripts/weekly-report.py" && bash "$SKILL_DIR/scripts/build-dashboard.sh" ;;
  2) echo "Ask Claude in chat: 'Invoke delegate-creative for <platform>'." ;;
  3) read -p "Campaign slug: " slug; python3 "$SKILL_DIR/scripts/build-landing.py" "$slug" ;;
  4) python3 "$SKILL_DIR/scripts/lead-lifecycle-deploy.py" ;;
  5) python3 "$SKILL_DIR/scripts/build-calendar.py" ;;
  6) python3 "$SKILL_DIR/scripts/monthly-strategy.py" && bash "$SKILL_DIR/scripts/build-dashboard.sh" ;;
  7) read -p "URL: " url; bash "$SKILL_DIR/scripts/discover.sh" "$url" && python3 "$SKILL_DIR/scripts/voice-fingerprint.py" ;;
  8) bash "$SKILL_DIR/scripts/install-mcp/connect-all.sh" ;;
  q|*) echo "Bye."; exit 0 ;;
esac

echo
echo "📊 Dashboard: ~/marketing/"
