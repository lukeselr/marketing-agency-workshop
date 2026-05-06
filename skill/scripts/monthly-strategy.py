#!/usr/bin/env python3
"""Phase 12 — Monthly strategy review.

Aggregates last 4 weekly reports into a 1-page deck, evaluates wedge performance,
detects competitor deltas (vs 30 days ago), recommends 70/20/10 budget rebalance,
ranks 3 wedge bets for next 30 days.
"""

from __future__ import annotations
import datetime as dt
import json
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
DASH = Path.home() / "marketing"


def last_4_reports() -> list:
    reports = sorted((DASH / "reports").glob("*.json"), reverse=True)
    out = []
    for r in reports[:4]:
        try:
            out.append(json.loads(r.read_text()))
        except Exception:
            pass
    return out


def main():
    today = dt.date.today()
    month = today.strftime("%Y-%m")
    reports = last_4_reports()

    deck = {
        "month": month,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "weeks_analysed": len(reports),
        "trend": {
            "spend_trend": [r.get("totals", {}).get("spend", 0) for r in reports],
            "leads_trend": [r.get("totals", {}).get("leads", 0) for r in reports],
            "cpa_trend": [r.get("totals", {}).get("cpa", 0) for r in reports],
        },
        "wedge_evaluation": {
            "delegate_to": "competitive-cartographer (re-run vs 30 days ago)",
            "result": "TBD by delegate run",
        },
        "competitor_delta": {
            "delegate_to": "delegate-competitor-watch",
            "result": "TBD by delegate run",
        },
        "budget_rebalance": {
            "framework": "70/20/10 from claude-ads/skills/ads-budget",
            "current_split": "computed at runtime",
            "recommended_split": "computed at runtime",
        },
        "next_30_day_bets": [
            {"rank": 1, "bet": "TBD", "rationale": "TBD", "expected_impact": "TBD"},
            {"rank": 2, "bet": "TBD", "rationale": "TBD", "expected_impact": "TBD"},
            {"rank": 3, "bet": "TBD", "rationale": "TBD", "expected_impact": "TBD"},
        ],
        "delivery_channels": ["PDF (via pdf skill)", "5-min Loom-style narration script", "Notion page (via notion-automation)"],
        "status": "drafted",
        "next": "Invoke `monthly-strategy-orchestrator` agent. It fills TBDs via delegate calls + renders PDF + Notion.",
    }

    reports_dir = DASH / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_json = reports_dir / f"{month}-monthly.json"
    out_json.write_text(json.dumps(deck, indent=2))

    # Markdown deck preview
    md_lines = [
        f"# Monthly strategy — {month}",
        "",
        f"_Generated {today.isoformat()} · {len(reports)} weekly reports analysed_",
        "",
        "## 30-day trend",
        f"- Spend by week: {deck['trend']['spend_trend']}",
        f"- Leads by week: {deck['trend']['leads_trend']}",
        f"- CPA by week: {deck['trend']['cpa_trend']}",
        "",
        "## Wedge evaluation",
        "- Pending `competitive-cartographer` re-run.",
        "",
        "## Competitor delta",
        "- Pending `delegate-competitor-watch` run.",
        "",
        "## Budget rebalance (70/20/10)",
        "- Pending `claude-ads/skills/ads-budget` evaluation.",
        "",
        "## Next 30-day bets",
        "1. TBD",
        "2. TBD",
        "3. TBD",
        "",
        "_Run `monthly-strategy-orchestrator` to populate TBDs._",
    ]
    out_md = reports_dir / f"{month}-monthly.md"
    out_md.write_text("\n".join(md_lines))

    print(f"[ok] {out_json}")
    print(f"[ok] {out_md}")


if __name__ == "__main__":
    main()
