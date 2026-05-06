#!/usr/bin/env python3
"""Cloud-drive scan stub. Defers to the Google Drive MCP / `google-drive-automation` skill.

This scraper does NOT actively scan — that requires consented MCP access in the calling
Claude Code session. It emits a recipe block that the orchestrator follows to do the
read-only scan, and a status flag so synthesise.py knows to skip silently when consent
hasn't been granted yet.
"""

from __future__ import annotations

import os
import sys

from _helpers import emit, normalise_input


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    consented = os.environ.get("MARKETING_AGENCY_DRIVE_CONSENTED", "").lower() in {"1", "yes", "true"}

    emit({
        "scraper": "cloud-drives",
        "status": "consent_required" if not consented else "deferred_to_mcp",
        "input": inp,
        "instructions": (
            "Phase 1 cloud-drive scan is read-only and consented. Run via the Google Drive MCP "
            "or `google-drive-automation` skill. Looks for: brand assets, logo files, customer "
            "lists, past creative, testimonials, contracts. Set MARKETING_AGENCY_DRIVE_CONSENTED=1 "
            "after the user confirms in chat."
        ),
        "consent_required": not consented,
        "needs_mcp": True,
    })


if __name__ == "__main__":
    main()
