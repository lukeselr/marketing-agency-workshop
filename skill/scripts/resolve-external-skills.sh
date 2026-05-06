#!/usr/bin/env bash
# Phase -1: resolve external skill dependencies.
#
# Each entry under references/external/ is a symlink to a sibling Claude Code
# skill that this orchestrator delegates to. On a fresh Mac many of those
# targets won't exist yet — half the orchestrator would silently no-op when
# delegating.
#
# This script:
#   1. Walks every symlink in references/external/
#   2. For each whose target is missing, tries to auto-resolve in this order:
#        a. ~/.claude/skills/<name>             (skills already installed on this machine)
#        b. ~/.marketing-agency/external/<name> (fallback path, populated by clone)
#        c. $MA_EXTERNAL_KIT_REPO clone via gh, if set + gh CLI auth-ed
#           (e.g. export MA_EXTERNAL_KIT_REPO=org/private-skill-bundle)
#   3. Records anything still missing in .state/missing-external.json so delegate
#      agents can graceful-skip with a plain-English note to the owner.
#
# Idempotent. Safe to re-run. Never fails the install.

set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
EXT_DIR="$SKILL_DIR/references/external"
STATE_DIR="$SKILL_DIR/.state"
FALLBACK_ROOT="$HOME/.marketing-agency/external"
LOG="$STATE_DIR/resolve-external.log"

mkdir -p "$STATE_DIR" "$FALLBACK_ROOT"
: > "$LOG"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "$(ts) $*" >> "$LOG"; }

if [ ! -d "$EXT_DIR" ]; then
  log "no references/external dir — nothing to resolve"
  echo '{"version":1,"missing":[],"resolved":[],"checked_at":"'"$(ts)"'"}' > "$STATE_DIR/missing-external.json"
  exit 0
fi

# Optional clone step: only runs if BOTH (a) gh CLI is auth-ed AND
# (b) MA_EXTERNAL_KIT_REPO env var is set. Workshop attendees leave this unset
# and the script just records misses for graceful-skip.
CAN_CLONE=0
EXT_REPO="${MA_EXTERNAL_KIT_REPO:-}"
if [ -n "$EXT_REPO" ] && command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then
    CAN_CLONE=1
    log "gh CLI authed and MA_EXTERNAL_KIT_REPO=$EXT_REPO — clone fallback enabled"
  else
    log "gh CLI present but not authed — skipping clone"
  fi
fi

# If we can clone and the kit isn't already on disk, do a shallow clone now.
KIT_DIR="$FALLBACK_ROOT/external-kit"
if [ "$CAN_CLONE" = "1" ] && [ ! -d "$KIT_DIR/.git" ]; then
  log "cloning $EXT_REPO -> $KIT_DIR"
  if gh repo clone "$EXT_REPO" "$KIT_DIR" -- --depth 1 >>"$LOG" 2>&1; then
    log "kit clone OK"
  else
    log "kit clone FAILED (likely no read access) — falling back to per-skill detection"
    rm -rf "$KIT_DIR" 2>/dev/null
  fi
fi

resolved=()
missing=()

for link in "$EXT_DIR"/*; do
  [ -L "$link" ] || continue
  name="$(basename "$link")"
  target="$(readlink "$link")"

  # Already valid? Skip.
  if [ -d "$target" ] || [ -d "$link/" ] && [ -f "$link/SKILL.md" ]; then
    resolved+=("$name")
    continue
  fi

  # Try the canonical user-skill path
  primary="$HOME/.claude/skills/$name"
  if [ -d "$primary" ] && { [ -f "$primary/SKILL.md" ] || [ -d "$primary/skills" ] || [ -f "$primary/README.md" ]; }; then
    rm -f "$link"
    ln -s "$primary" "$link"
    resolved+=("$name")
    log "$name -> $primary (primary)"
    continue
  fi

  # Try attendee fallback path
  fallback="$FALLBACK_ROOT/$name"
  if [ -d "$fallback" ] && { [ -f "$fallback/SKILL.md" ] || [ -d "$fallback/skills" ] || [ -f "$fallback/README.md" ]; }; then
    rm -f "$link"
    ln -s "$fallback" "$link"
    resolved+=("$name")
    log "$name -> $fallback (fallback)"
    continue
  fi

  # Try kit subdirectories (kit may keep skills under skills/<name>/)
  if [ -d "$KIT_DIR" ]; then
    for candidate in "$KIT_DIR/skills/$name" "$KIT_DIR/$name"; do
      if [ -d "$candidate" ] && { [ -f "$candidate/SKILL.md" ] || [ -d "$candidate/skills" ] || [ -f "$candidate/README.md" ]; }; then
        rm -f "$link"
        ln -s "$candidate" "$link"
        resolved+=("$name")
        log "$name -> $candidate (kit)"
        break
      fi
    done
    if printf '%s\n' "${resolved[@]:-}" | grep -qx "$name"; then
      continue
    fi
  fi

  missing+=("$name")
  log "$name MISSING (link broken, no fallback)"
done

# Build missing-external.json
{
  echo '{'
  echo '  "version": 1,'
  echo '  "checked_at": "'"$(ts)"'",'
  echo '  "kit_dir": "'"$KIT_DIR"'",'
  echo '  "kit_present": '"$([ -d "$KIT_DIR" ] && echo true || echo false)"','
  echo -n '  "resolved": ['
  first=1
  for n in "${resolved[@]:-}"; do
    [ -z "$n" ] && continue
    if [ "$first" = "1" ]; then first=0; else printf ', '; fi
    printf '"%s"' "$n"
  done
  echo '],'
  echo -n '  "missing": ['
  first=1
  for n in "${missing[@]:-}"; do
    [ -z "$n" ] && continue
    if [ "$first" = "1" ]; then first=0; else printf ', '; fi
    printf '"%s"' "$n"
  done
  echo ']'
  echo '}'
} > "$STATE_DIR/missing-external.json"

R=${#resolved[@]}; M=${#missing[@]}
echo "external skills: ${R} resolved, ${M} missing"
if [ "$M" -gt 0 ]; then
  echo "missing: ${missing[*]}"
  echo "  → delegate agents will graceful-skip these and surface a plain-English note to the owner."
  echo "  → if you have a private skill kit you can clone, set MA_EXTERNAL_KIT_REPO=<org>/<repo>, run \`gh auth login\`, then re-run \`bash install.sh\`."
fi
exit 0
