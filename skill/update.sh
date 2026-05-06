#!/usr/bin/env bash
# Pull latest marketing-agency release from GitHub. Runs migration script.
set -u
REPO="${MA_REPO:-lukeselr/marketing-agency-workshop}"
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
TMP=$(mktemp -d)
cd "$TMP"

if command -v gh > /dev/null; then
  gh repo clone "$REPO" .
else
  git clone "https://github.com/$REPO" .
fi

if [ -d "skill" ]; then
  bash install.sh
elif [ -d "skills/marketing-agency" ]; then
  bash skills/marketing-agency/install.sh
elif [ -d "marketing-agency" ]; then
  bash marketing-agency/install.sh
fi

CUR_VER=$(cat "$SKILL_DIR/VERSION" 2>/dev/null || echo "?")
echo "Updated to: $CUR_VER"
rm -rf "$TMP"
