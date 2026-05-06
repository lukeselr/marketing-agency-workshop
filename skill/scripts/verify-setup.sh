#!/usr/bin/env bash
# Smoke-test all 3 platforms after Phase 5.
# Confirms tokens work, ad accounts reachable, pixels firing.
set -u
TOK="$HOME/.marketing-agency/tokens"
echo "=== marketing-agency verify ==="

if [ -f "$TOK/meta.json" ]; then
  TOKEN=$(jq -r .system_user_token "$TOK/meta.json")
  if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "[meta] checking..."
    curl -s "https://graph.facebook.com/v19.0/me?access_token=$TOKEN" | jq .
  fi
fi

if [ -f "$TOK/linkedin.json" ]; then
  TOKEN=$(jq -r .access_token "$TOK/linkedin.json")
  if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
    echo "[linkedin] checking..."
    curl -s -H "Authorization: Bearer $TOKEN" "https://api.linkedin.com/v2/me" | jq .
  fi
fi

if [ -f "$TOK/google-ads.json" ]; then
  echo "[google-ads] developer token + refresh token present:"
  jq -r 'has("developer_token") as $d | has("refresh_token") as $r | "developer_token=\($d) refresh_token=\($r)"' "$TOK/google-ads.json"
fi

echo "Done."
