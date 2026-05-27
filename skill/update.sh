#!/usr/bin/env bash
# Pull latest marketing-agency release from GitHub. Runs migration script.
# MA_REPO overrides the repo. MA_REF pins a tag/branch/sha — strongly
# recommended for production installs so a broken main can't auto-update you.
set -u
REPO="${MA_REPO:-lukeselr/marketing-agency-workshop}"
REF="${MA_REF:-main}"
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
TMP=$(mktemp -d)
cd "$TMP"

if [ "$REF" = "main" ]; then
  echo "WARN: tracking 'main' branch — set MA_REF=<tag> (e.g. MA_REF=v2.1.1) to pin."
fi

if command -v gh > /dev/null; then
  gh repo clone "$REPO" . -- --branch "$REF" --depth 1 || gh repo clone "$REPO" .
else
  git clone --branch "$REF" --depth 1 "https://github.com/$REPO" . 2>/dev/null \
    || git clone "https://github.com/$REPO" .
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
