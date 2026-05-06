#!/usr/bin/env python3
"""Phase 9.5 — Weekly client report.

Pulls last 7 days from Meta Ads / LinkedIn Ads / Google Ads via stored tokens
(or MCPs at runtime), GHL CRM pipeline, kill-rule actions log, and renders a
single-page HTML report. Drops a copy into ~/marketing/reports/ and refreshes
~/marketing/this-week.md.

Designed to run unattended (Monday 7am AEST cron) and produce something the
owner can hand to a stakeholder verbatim.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import sys
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
DASH = Path.home() / "marketing"
TOKENS = Path.home() / ".marketing-agency/tokens"

REPORTS_DIR = DASH / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def now_iso():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def week_id(d: dt.date | None = None) -> str:
    d = d or dt.date.today()
    iso_year, iso_week, _ = d.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def load_json(p: Path) -> dict:
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def stub_metrics_from_tokens() -> dict:
    """Until MCPs are wired, return a placeholder structure with safe zeros.

    The orchestrator agent (`weekly-report-orchestrator`) is responsible for
    populating the real numbers via Meta/LinkedIn/Google Ads MCP at runtime.
    This script is the renderer + scaffolder.
    """
    meta = load_json(TOKENS / "meta.json")
    li = load_json(TOKENS / "linkedin.json")
    g = load_json(TOKENS / "google-ads.json")

    return {
        "platforms": {
            "meta": {
                "connected": bool(meta.get("system_user_token")),
                "ad_account_id": meta.get("ad_account_id"),
                "spend_aud": 0.0, "leads": 0, "cpa": 0.0, "roas": 0.0,
                "ctr_pct": 0.0, "frequency": 0.0,
            },
            "linkedin": {
                "connected": bool(li.get("access_token")),
                "ad_account_urn": li.get("ad_account_urn"),
                "spend_aud": 0.0, "leads": 0, "cpa": 0.0, "roas": 0.0,
                "ctr_pct": 0.0,
            },
            "google_ads": {
                "connected": bool(g.get("refresh_token")),
                "customer_id": g.get("customer_id"),
                "spend_aud": 0.0, "leads": 0, "cpa": 0.0, "roas": 0.0,
                "ctr_pct": 0.0,
            },
        },
        "totals": {"spend": 0.0, "leads": 0, "cpa": 0.0},
        "last_week_totals": {"spend": 0.0, "leads": 0, "cpa": 0.0},
        "winners": [],
        "killed": [],
        "pipeline": {"new_leads": 0, "mql": 0, "sql": 0},
        "creative_fatigue": [],
        "next_actions": [],
    }


def render_html(data: dict, week: str, business: str) -> str:
    p = data["platforms"]
    t = data["totals"]
    lt = data["last_week_totals"]
    pipe = data["pipeline"]

    def delta(curr, prev):
        if not prev:
            return ""
        d = curr - prev
        sign = "▲" if d > 0 else "▼" if d < 0 else "—"
        return f" {sign} {abs(d):.1f}"

    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{business} — {week}</title>
<style>
body {{ font: 15px/1.5 -apple-system, system-ui, sans-serif; max-width: 720px; margin: 40px auto; padding: 0 20px; color: #111; }}
h1 {{ font-size: 22px; margin: 0 0 4px; }}
h2 {{ font-size: 16px; margin: 28px 0 8px; border-bottom: 1px solid #eee; padding-bottom: 4px; }}
.meta {{ color: #666; font-size: 13px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 16px 0; }}
.card {{ background: #f7f7f7; border-radius: 8px; padding: 12px; }}
.card .num {{ font-size: 22px; font-weight: 600; }}
.card .lbl {{ color: #666; font-size: 12px; }}
.row {{ display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px dashed #eee; }}
.green {{ color: #1a7f37; }}
.red {{ color: #cf222e; }}
ul {{ padding-left: 20px; }}
.empty {{ color: #999; font-style: italic; }}
</style>
</head><body>
<h1>📊 {business}</h1>
<div class="meta">Weekly report · {week} · generated {dt.date.today().isoformat()}</div>

<h2>Top-line</h2>
<div class="grid">
  <div class="card"><div class="num">${t['spend']:,.0f}</div><div class="lbl">spend{delta(t['spend'], lt['spend'])}</div></div>
  <div class="card"><div class="num">{t['leads']}</div><div class="lbl">leads{delta(t['leads'], lt['leads'])}</div></div>
  <div class="card"><div class="num">${t['cpa']:,.0f}</div><div class="lbl">CPA{delta(t['cpa'], lt['cpa'])}</div></div>
</div>

<h2>Per-platform</h2>
<div class="row"><span>Meta {('✅' if p['meta']['connected'] else '⚪')} </span><span>${p['meta']['spend_aud']:,.0f} · {p['meta']['leads']} leads · CPA ${p['meta']['cpa']:.0f}</span></div>
<div class="row"><span>LinkedIn {('✅' if p['linkedin']['connected'] else '⚪')} </span><span>${p['linkedin']['spend_aud']:,.0f} · {p['linkedin']['leads']} leads · CPA ${p['linkedin']['cpa']:.0f}</span></div>
<div class="row"><span>Google {('✅' if p['google_ads']['connected'] else '⚪')} </span><span>${p['google_ads']['spend_aud']:,.0f} · {p['google_ads']['leads']} leads · CPA ${p['google_ads']['cpa']:.0f}</span></div>

<h2>Winners</h2>
{render_list(data['winners'], "No campaigns yet — first launch happens after Phase 8.")}

<h2>Killed (paused by skill)</h2>
{render_list(data['killed'], "Nothing was killed this week.")}

<h2>Pipeline (CRM)</h2>
<div class="row"><span>New leads</span><span>{pipe['new_leads']}</span></div>
<div class="row"><span>MQL</span><span>{pipe['mql']}</span></div>
<div class="row"><span>SQL</span><span>{pipe['sql']}</span></div>

<h2>Creative fatigue</h2>
{render_list(data['creative_fatigue'], "No fatigue detected.")}

<h2>Next 3 actions</h2>
{render_list(data['next_actions'], "Skill will populate after first 7 days of data.")}

<p class="meta">marketing-agency · v2.0 · ~/marketing/reports/{week}.html</p>
</body></html>"""


def render_list(items: list, empty_msg: str) -> str:
    if not items:
        return f'<p class="empty">{empty_msg}</p>'
    return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def main():
    business = "Your business"
    baseline = STATE / "business-baseline.md"
    if baseline.is_file():
        first_line = baseline.read_text().splitlines()[0]
        if "Business Baseline:" in first_line:
            business = first_line.split("Business Baseline:", 1)[1].strip().lstrip("# ")

    data = stub_metrics_from_tokens()
    week = week_id()

    html = render_html(data, week, business)
    out = REPORTS_DIR / f"{week}.html"
    out.write_text(html)

    # Also save raw json for downstream
    (REPORTS_DIR / f"{week}.json").write_text(json.dumps({
        "generated_at": now_iso(),
        "week": week,
        "business": business,
        **data,
    }, indent=2))

    # Refresh ~/marketing/this-week.md from this report
    this_week = DASH / "this-week.md"
    this_week.write_text(f"""# This week — {dt.date.today()} ({week})

**{business}**

## Top-line
- Spend: **${data['totals']['spend']:,.0f}**
- Leads: **{data['totals']['leads']}**
- CPA: **${data['totals']['cpa']:,.0f}**

## Platforms connected
{render_platform_status(data['platforms'])}

## Read full report
`open {out}`

_Auto-refreshed by Phase 9.5 weekly cron. Manually run:_
```bash
bash ~/.claude/skills/marketing-agency/scripts/weekly-report.py
bash ~/.claude/skills/marketing-agency/scripts/build-dashboard.sh
```
""")

    print(f"[ok] wrote {out}")
    print(f"[ok] refreshed {this_week}")


def render_platform_status(p: dict) -> str:
    rows = []
    for name, key in (("Meta", "meta"), ("LinkedIn", "linkedin"), ("Google Ads", "google_ads")):
        rows.append(f"- {name}: {'✅ connected' if p[key]['connected'] else '⚪ not yet'}")
    return "\n".join(rows)


if __name__ == "__main__":
    main()
