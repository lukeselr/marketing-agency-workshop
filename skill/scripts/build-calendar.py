#!/usr/bin/env python3
"""Phase 11 — Organic content calendar.

Pulls top 3 paid winners from latest weekly report + voice fingerprint, drafts
30 posts across LinkedIn / IG / FB / X / TikTok using social-orchestrator and
carousel-generator skills (delegated at runtime). Outputs a calendar plan.
"""

from __future__ import annotations
import datetime as dt
import json
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
DASH = Path.home() / "marketing"


def latest_weekly_winners() -> list:
    reports = sorted((DASH / "reports").glob("*.json"), reverse=True)
    if not reports:
        return []
    try:
        return (json.loads(reports[0].read_text()).get("winners") or [])[:3]
    except Exception:
        return []


def main():
    winners = latest_weekly_winners()
    today = dt.date.today()
    calendar = []
    # 30 posts spread over next 30 days, mix of platforms + formats
    formats = [
        ("linkedin", "thought-leader-post"),
        ("instagram", "carousel"),
        ("instagram", "reel-script"),
        ("facebook", "post"),
        ("twitter", "thread"),
        ("tiktok", "video-script"),
    ]
    for i in range(30):
        day = today + dt.timedelta(days=i)
        fmt = formats[i % len(formats)]
        calendar.append({
            "date": day.isoformat(),
            "platform": fmt[0],
            "format": fmt[1],
            "topic_seed": (
                f"Repurpose paid-ad winner #{(i % 3) + 1}: {winners[i % 3]['headline'] if winners and i < 3*len(winners) else 'TBD'}"
                if winners else
                "Owner-supplied topic OR auto-pull from voice-fingerprint top vocab"
            ),
            "status": "draft",
        })

    plan = {
        "month_start": today.isoformat(),
        "post_count": len(calendar),
        "winners_seeded": len(winners),
        "calendar": calendar,
        "delegates": [
            "social-orchestrator (cross-platform formatting)",
            "carousel-generator (IG carousels)",
            "social-content (short-form copy)",
            "content-marketer (long-form blog repurposing)",
            "apify-content-analytics (best-time-to-post + hashtags)",
            "notion-automation (push to Notion calendar)",
        ],
        "status": "drafted",
        "next": "Invoke `delegate-organic-calendar` agent. It produces actual copy + carousels and pushes to Notion.",
    }
    out = STATE / "content-calendar.json"
    out.write_text(json.dumps(plan, indent=2))

    # Also drop a human-readable preview into ~/marketing/calendar/this-month.md
    cal_dir = DASH / "calendar"
    cal_dir.mkdir(parents=True, exist_ok=True)
    md = ["# Content calendar — next 30 days", "", f"_Generated {today.isoformat()}_", ""]
    md.append("| Date | Platform | Format | Topic |")
    md.append("|---|---|---|---|")
    for p in calendar:
        md.append(f"| {p['date']} | {p['platform']} | {p['format']} | {p['topic_seed']} |")
    (cal_dir / "this-month.md").write_text("\n".join(md))

    print(f"[ok] calendar at {out}")
    print(f"[ok] preview at {cal_dir / 'this-month.md'}")


if __name__ == "__main__":
    main()
