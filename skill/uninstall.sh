#!/usr/bin/env bash
# marketing-agency uninstaller. Leaves ~/.marketing-agency/tokens/ untouched (user data).
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
read -p "Remove $SKILL_DIR? [y/N] " yn
case "$yn" in
  [Yy]*) rm -rf "$SKILL_DIR"; echo "Removed.";;
  *) echo "Cancelled.";;
esac
echo "Tokens preserved at ~/.marketing-agency/tokens/. Remove manually if you want."
