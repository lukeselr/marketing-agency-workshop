#!/usr/bin/env bash
# Polls Gmail for approval emails sent to the owner and advances `.state/approvals.json`
# when a reply containing "APPROVED" arrives. Runs every 12h via cron (deployed by Phase 9).
#
# Approval email format (sent by the orchestrator when a phase needs a green-light):
#   Subject: [marketing-agency] Approve: <campaign-name>
#   Body:    Reply YES or APPROVED to launch.
# The owner replies in plain English; this script picks up the reply, marks the
# corresponding approval token as accepted, and the next orchestrator tick proceeds.

set -u

SKILL_DIR="$HOME/.claude/skills/marketing-agency"
STATE_DIR="$SKILL_DIR/.state"
APPROVALS="$STATE_DIR/approvals.json"
LOG="$STATE_DIR/poll-approvals.log"

mkdir -p "$STATE_DIR"
[ -f "$APPROVALS" ] || echo '{"version":1,"pending":[],"approved":[],"rejected":[]}' > "$APPROVALS"

ts() { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
log() { echo "$(ts) $*" >> "$LOG"; }

log "poll-approvals start"

# We use the Gmail MCP via `claude` CLI in a one-shot non-interactive call.
# If `claude` isn't available, we skip silently — orchestrator will use the older
# manual approval path (owner runs `bash scripts/resume.sh approved <token>`).
if ! command -v claude >/dev/null 2>&1; then
  log "no claude CLI — skip"
  exit 0
fi

PROMPT='You are a non-interactive helper. Use the Gmail MCP to search the inbox for messages with subject containing "[marketing-agency] Approve" received in the last 7 days. For each such message, fetch the latest reply on the thread and report ONLY a JSON array of objects: [{"token":"<extracted token from subject or body>","decision":"approved|rejected|pending","ts":"<iso>"}]. Do not narrate. Do not include code fences. If nothing found, return [].'

REPLY=$(claude -p --output-format text "$PROMPT" 2>>"$LOG" || echo "[]")
# Strip anything before the first [ to be safe
REPLY=$(echo "$REPLY" | sed -n '/^\[/,$p')
[ -z "$REPLY" ] && REPLY="[]"

# Validate JSON
if ! echo "$REPLY" | jq -e 'type == "array"' >/dev/null 2>&1; then
  log "invalid JSON from claude — abort"
  exit 0
fi

# Merge into approvals.json
TMP=$(mktemp)
jq --argjson new "$REPLY" '
  . as $cur |
  reduce $new[] as $item ($cur;
    if $item.decision == "approved" then
      .approved += [$item] | .pending = (.pending - [.pending[] | select(.token == $item.token)])
    elif $item.decision == "rejected" then
      .rejected += [$item] | .pending = (.pending - [.pending[] | select(.token == $item.token)])
    else . end)
' "$APPROVALS" > "$TMP" && mv "$TMP" "$APPROVALS"

NEW_OK=$(echo "$REPLY" | jq '[.[] | select(.decision=="approved")] | length')
NEW_NO=$(echo "$REPLY" | jq '[.[] | select(.decision=="rejected")] | length')
log "merged: +${NEW_OK} approved, +${NEW_NO} rejected"

echo "ok ${NEW_OK} approved, ${NEW_NO} rejected"
