#!/usr/bin/env bash
# marketing-agency installer (Mac/Linux). v2.1
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
SRC="$(cd "$(dirname "$0")" && pwd)"

echo "Installing marketing-agency v$(cat "$SRC/VERSION") to $SKILL_DIR"
mkdir -p "$SKILL_DIR"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude '.state' --exclude 'dist' \
    --exclude '__pycache__' --exclude 'node_modules' \
    --exclude '.env' \
    "$SRC/" "$SKILL_DIR/"
else
  (cd "$SRC" && tar --exclude='.state' --exclude='dist' --exclude='__pycache__' \
    --exclude='node_modules' --exclude='.env' -cf - .) | \
  (cd "$SKILL_DIR" && tar -xf -)
fi

mkdir -p "$HOME/.marketing-agency/tokens"
chmod 700 "$HOME/.marketing-agency" "$HOME/.marketing-agency/tokens"

# Capture MA_BUSINESS_NAME once at install time. Used as the default base for
# every account/app/form name the Playwright specs create (MCC, OAuth, lead
# forms, LinkedIn dev app). Written to the skill-local .env file so the specs
# pick it up automatically via Playwright's dotenv loader.
# Non-interactive shells (CI, piped install) silently skip and the specs fall
# back to neutral placeholders like "My Agency MCC".
SKILL_ENV_FILE="$SKILL_DIR/.env"
if [ ! -f "$SKILL_ENV_FILE" ] && [ -t 0 ] && [ -z "${MA_NONINTERACTIVE:-}" ]; then
  printf "\nWhat's your business name? Used to label your Meta/Google/LinkedIn assets (press Enter to skip): "
  read -r MA_BIZ_INPUT
  if [ -n "$MA_BIZ_INPUT" ]; then
    umask 077
    {
      echo "# Captured at install time. Safe to edit. .gitignore excludes .env."
      echo "MA_BUSINESS_NAME=\"$MA_BIZ_INPUT\""
    } > "$SKILL_ENV_FILE"
    chmod 600 "$SKILL_ENV_FILE"
    echo "  Saved to $SKILL_ENV_FILE"
  fi
fi

# Auto-install Python deps. macOS 14+ / Ubuntu 23.04+ have PEP 668 lockdown,
# so we cascade --user -> --user --break-system-packages -> --break-system-packages
# until one works.
if command -v pip3 >/dev/null 2>&1; then
  echo "Installing Python deps..."
  if pip3 install --user --quiet beautifulsoup4 requests 2>/dev/null; then
    : # ok
  elif pip3 install --user --break-system-packages --quiet beautifulsoup4 requests 2>/dev/null; then
    echo "  (PEP 668 detected, used --break-system-packages)"
  elif pip3 install --break-system-packages --quiet beautifulsoup4 requests 2>/dev/null; then
    echo "  (PEP 668 detected, fell back to system pip)"
  else
    echo "  WARN: pip install failed. Phase 1 scrapers may run in degraded mode."
    echo "  Manual fix: pip3 install --break-system-packages beautifulsoup4 requests"
  fi
fi

# Run pre-flight
bash "$SKILL_DIR/scripts/check-preflight.sh" || {
  echo
  echo "Pre-flight reported blockers — install partially complete. Fix and re-run."
  exit 1
}

# Resolve external skill dependencies (graceful for non-Selr machines)
echo
echo "==> Resolving external skill dependencies"
bash "$SKILL_DIR/scripts/resolve-external-skills.sh" || true

# Build dashboard scaffold
bash "$SKILL_DIR/scripts/build-dashboard.sh"

# Connect every MCP we delegate to
echo
echo "==> Wiring MCPs (Playwright, Meta, LinkedIn, GHL, Notion, Slack, etc)"
bash "$SKILL_DIR/scripts/install-mcp/connect-all.sh"

# Install slash command. The skill ships with its own commands/marketing-agency.md
# that we copy into the user-level Claude Code commands dir. Always overwrite so
# attendees get the latest version on every install.
SLASH_DIR="$HOME/.claude/commands"
SLASH_SRC="$SKILL_DIR/commands/marketing-agency.md"
if [ -f "$SLASH_SRC" ]; then
  mkdir -p "$SLASH_DIR"
  cp "$SLASH_SRC" "$SLASH_DIR/marketing-agency.md"
  echo "Slash command installed: type /marketing-agency in Claude Code"
fi

echo
echo "✅ Installed marketing-agency v$(cat "$SKILL_DIR/VERSION")"
echo
echo "Next: open Claude Code and type:"
echo "  /marketing-agency"
echo
echo "Or run end-to-end Phase 0 + Phase 1 directly:"
echo "  bash $SKILL_DIR/scripts/run.sh <YOUR_BUSINESS_URL>"
echo
echo "Your dashboard lives at:  ~/marketing/"
