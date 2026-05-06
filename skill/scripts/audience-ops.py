#!/usr/bin/env python3
"""Phase 8 audience-ops upgrade — auto-build retargeting, lookalike, exclusions.

Reads tokens, builds 3-tier audience structure per platform:
  - Retargeting: 180-day site visitors, 30-day engagers, customer-list match
  - Lookalike: 1% / 3% / 5% from hashed customer CSV
  - Exclusion: existing customers, recent purchasers (30d), bounced visitors

This script is the SCAFFOLDER. Real audience creation happens via Meta/LinkedIn/Google
Ads MCPs at runtime when delegate-creative invokes the matching ad-platform skill
(claude-ads/skills/ads-meta etc).
"""

from __future__ import annotations
import json
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
TOKENS = Path.home() / ".marketing-agency/tokens"


def main():
    plan = {
        "retargeting": {
            "site_visitors_180d": "All visitors via pixel",
            "page_engagers_30d": "Watched ≥50% video / scrolled ≥75% / clicked CTA",
            "customer_list": "Hashed CSV upload from GHL CRM (delegate to ghl-crm)",
        },
        "lookalike": {
            "lal_1pct": "1% from customer-list seed (hashed)",
            "lal_3pct": "3% — broader scaling",
            "lal_5pct": "5% — top-of-funnel reach",
            "seed_min_size": 1000,
            "seed_strategy": "Use top-LTV customers if available, else all customers",
        },
        "exclusions": {
            "existing_customers": "Hashed customer-list excluded from cold campaigns",
            "recent_purchasers_30d": "30-day window post-purchase",
            "bounced_visitors": "<5 sec session time excluded from remarketing",
        },
        "platforms": {
            "meta": {
                "tokens_present": (TOKENS / "meta.json").is_file(),
                "delegate_to": "claude-ads/skills/ads-meta",
            },
            "linkedin": {
                "tokens_present": (TOKENS / "linkedin.json").is_file(),
                "delegate_to": "claude-ads/skills/ads-linkedin",
            },
            "google_ads": {
                "tokens_present": (TOKENS / "google-ads.json").is_file(),
                "delegate_to": "claude-ads/skills/ads-google",
            },
        },
        "status": "drafted",
        "next": (
            "Invoke `delegate-creative` (or matching platform agent) "
            "with this plan + tokens to actually create audiences via MCP. "
            "Always set new audiences as INACTIVE; require owner review."
        ),
    }

    out = STATE / "audience-ops-plan.json"
    out.write_text(json.dumps(plan, indent=2))
    print(f"[ok] plan: {out}")


if __name__ == "__main__":
    main()
