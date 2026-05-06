#!/usr/bin/env bash
# marketing-agency-workshop installer.
# Module 3 of the Selr AI Workshop. Copies the marketing-agency skill into
# ~/.claude/skills/ and runs its internal installer.
#
# Idempotent. Safe to re-run.

set -u

SRC="$(cd "$(dirname "$0")" && pwd)"
SKILL_SRC="$SRC/skill"
SKILL_DST="$HOME/.claude/skills/marketing-agency"

if [ ! -d "$SKILL_SRC" ]; then
  echo "[fail] expected skill source at $SKILL_SRC"
  exit 1
fi

echo "==> Installing marketing-agency skill to $SKILL_DST"
mkdir -p "$(dirname "$SKILL_DST")"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '.state' --exclude 'dist' \
    --exclude '__pycache__' --exclude 'node_modules' \
    --exclude '.env' --exclude '*.pyc' \
    "$SKILL_SRC/" "$SKILL_DST/"
else
  rm -rf "$SKILL_DST"
  mkdir -p "$SKILL_DST"
  (cd "$SKILL_SRC" && tar -cf - .) | (cd "$SKILL_DST" && tar -xf -)
fi

echo "==> Running skill installer"
bash "$SKILL_DST/install.sh"

echo
echo "Module 3 install complete."
echo
echo "Next: in Claude Code, type"
echo "  /marketing-agency"
echo "and paste your business website URL when asked."
