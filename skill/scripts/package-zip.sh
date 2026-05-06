#!/usr/bin/env bash
# Build distributable zip. Excludes secrets, state, caches. Fails if any token pattern detected.
set -u
SKILL_DIR="$HOME/.claude/skills/marketing-agency"
OUT="$SKILL_DIR/dist/marketing-agency.zip"
mkdir -p "$(dirname "$OUT")"
rm -f "$OUT"

cd "$(dirname "$SKILL_DIR")"

# Secrets pattern check — bail if any token-shaped string in the tree (excluding examples)
LEAK=$(grep -rEn 'EAA[A-Za-z0-9]{40,}|sk-[A-Za-z0-9]{40,}|AIza[0-9A-Za-z_-]{35}' \
  marketing-agency \
  --exclude=env.example --exclude=.gitignore --exclude=audit-log.md 2>/dev/null || true)
if [ -n "$LEAK" ]; then
  echo "[fail] Token-shaped strings detected:"; echo "$LEAK"; exit 1
fi

zip -r "$OUT" marketing-agency \
  -x 'marketing-agency/.state/*' \
  -x 'marketing-agency/.state' \
  -x 'marketing-agency/dist/*' \
  -x 'marketing-agency/**/__pycache__/*' \
  -x 'marketing-agency/**/.playwright-cache/*' \
  -x 'marketing-agency/**/node_modules/*' \
  -x 'marketing-agency/**/.env'

SIZE=$(stat -f%z "$OUT" 2>/dev/null || stat -c%s "$OUT")
SIZE_MB=$(( SIZE / 1024 / 1024 ))
if [ "$SIZE_MB" -gt 5 ]; then
  echo "[fail] zip is ${SIZE_MB}MB > 5MB cap. Trim assets."; exit 1
fi
echo "[ok] $OUT (${SIZE_MB}MB)"
