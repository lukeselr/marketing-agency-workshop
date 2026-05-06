#!/usr/bin/env bash
# Unified token storage at ~/.marketing-agency/tokens/<platform>.json mode 600.
# Usage:
#   tokens-storage.sh write <platform> <key> <value>
#   tokens-storage.sh read <platform> <key>
#   tokens-storage.sh ensure-dir
set -u
TOK_DIR="$HOME/.marketing-agency/tokens"
mkdir -p "$TOK_DIR"
chmod 700 "$TOK_DIR"

cmd="${1:-}"
case "$cmd" in
  ensure-dir) exit 0 ;;
  write)
    platform="$2"; key="$3"; value="$4"
    file="$TOK_DIR/$platform.json"
    [ -f "$file" ] || echo '{}' > "$file"
    jq ".\"$key\" = \"$value\" | .platform = \"$platform\" | .version = 1" "$file" > "$file.tmp" && mv "$file.tmp" "$file"
    chmod 600 "$file"
    echo "[ok] wrote $platform.$key"
    ;;
  read)
    platform="$2"; key="$3"
    jq -r ".\"$key\" // empty" "$TOK_DIR/$platform.json" 2>/dev/null
    ;;
  *)
    echo "Usage: tokens-storage.sh {ensure-dir|write|read} <args>"; exit 1 ;;
esac
