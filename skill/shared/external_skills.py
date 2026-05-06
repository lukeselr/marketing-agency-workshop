"""Helper for delegate-* agents to graceful-skip when an external skill is missing.

Usage in scripts/agents:

    from shared.external_skills import is_available, skip_note

    if not is_available("ghl-landing-pages"):
        print(skip_note("ghl-landing-pages", task="build the landing page"))
        return

The owner-facing skip note is plain English (no jargon, no em dashes) and
matches the firewall config used by other voice-graded outputs.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

SKILL_ROOT = Path.home() / ".claude/skills/marketing-agency"
STATE_FILE = SKILL_ROOT / ".state/missing-external.json"


def _load() -> dict:
    if not STATE_FILE.is_file():
        return {"missing": [], "resolved": []}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {"missing": [], "resolved": []}


def is_available(skill_name: str) -> bool:
    """True if `references/external/<skill_name>` is wired up on this machine."""
    data = _load()
    if skill_name in data.get("resolved", []):
        return True
    if skill_name in data.get("missing", []):
        return False
    # Unknown skill (e.g. caller typo) — fall back to filesystem check.
    link = SKILL_ROOT / "references/external" / skill_name
    if not link.exists():
        return False
    target = link.resolve()
    return target.exists() and target.is_dir()


def missing_skills() -> list[str]:
    return list(_load().get("missing", []))


def skip_note(skill_name: str, task: str) -> str:
    """Plain-English message the orchestrator surfaces to the owner.

    No em dashes. No jargon. Tells the owner exactly what to do next.
    """
    return (
        f"[skipped] We would normally use the `{skill_name}` skill to {task}, "
        f"but it is not installed on this machine. We are continuing without it.\n"
        f"To turn this on later, install the `{skill_name}` skill into "
        f"`~/.claude/skills/{skill_name}/` and re-run `bash ~/.claude/skills/marketing-agency/install.sh`."
    )


def require(skills: Iterable[str]) -> tuple[list[str], list[str]]:
    """Return (available, unavailable) split for a set of required skills."""
    available = []
    unavailable = []
    for s in skills:
        (available if is_available(s) else unavailable).append(s)
    return available, unavailable
