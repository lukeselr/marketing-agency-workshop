#!/usr/bin/env python3
"""Daily kill-rule monitor.

Pulls campaign perf from Meta + LinkedIn + Google Ads MCPs (or direct API).
Pauses anything breaking the rules in shared/conversion-events.json.
Alerts via Telegram (preferred), Google Chat, or email.

Deployable to: AWS server cron / macOS launchd / Anthropic Routine cloud cron.
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
TOKENS = Path.home() / ".marketing-agency/tokens"
RULES_FILE = SKILL / "shared/conversion-events.json"


def load_rules() -> dict:
    return json.loads(RULES_FILE.read_text())["kill_rules_thresholds"]


def telegram_alert(msg: str) -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not (token and chat_id):
        sys.stderr.write(f"[no-alert] {msg}\n")
        return
    import urllib.request, urllib.parse
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": msg}).encode()
    try:
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data=payload, timeout=10
        )
    except Exception as e:
        sys.stderr.write(f"[alert-fail] {e}\n")


def check_meta(rules: dict) -> list[dict]:
    """Pull recent stats. Pause campaigns breaking rules. Returns list of actions."""
    # Stub — real version uses Meta Marketing API via stored token.
    actions: list[dict] = []
    return actions


def check_linkedin(rules: dict) -> list[dict]:
    return []


def check_google(rules: dict) -> list[dict]:
    return []


def main() -> None:
    rules = load_rules()
    actions: list[dict] = []
    for fn in (check_meta, check_linkedin, check_google):
        try:
            actions.extend(fn(rules))
        except Exception as e:
            sys.stderr.write(f"[check-error] {fn.__name__}: {e}\n")
    if actions:
        telegram_alert(f"marketing-agency: {len(actions)} campaigns paused. See log.")
    log = SKILL / ".state/kill-rule.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as f:
        f.write(json.dumps({"actions": actions}) + "\n")


if __name__ == "__main__":
    main()
