#!/usr/bin/env python3
"""Phase 10 — Deploy lead lifecycle automation.

Builds: instant SMS reply, instant email reply, day-0/1/3/7/14/30 drip,
no-show recovery (3hr + 24hr), lead-scoring custom-field, hot-lead Slack ping.

This script is the SCAFFOLDER. The actual GHL workflow + ManyChat flow + email
deployment is delegated at runtime to `delegate-email-drip` + `delegate-sms-instant`
agents using the templates this script writes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
TEMPLATES = SKILL / "templates/lifecycle-sequences"


INDUSTRY_RULES = [
    # Highest-specificity first — the matcher returns on first hit
    (("buyer's agent", "buyers agent", "buyers-agent", "property buyer"), "buyers-agent"),
    (("mortgage broker", "home loan broker", "finance broker"), "mortgage-broker"),
    (("financial planner", "financial advisor", "financial adviser", "wealth manager"), "financial-planner"),
    (("dentist", "dental", "orthodontist"), "dentist"),
    (("salon", "hairdresser", "beauty salon", "barber"), "salon"),
    (("gym", "f45", "crossfit", "personal training", "fitness studio"), "gym"),
    (("cafe", "café", "coffee shop", "espresso bar"), "cafe"),
    (("tradesperson", "tradie", "builder", "plumber", "electrician", "carpenter", "trade"), "trades"),
    (("real estate", "real-estate", "realtor", "estate agent"), "real-estate"),
    (("hospitality", "restaurant", "bistro", "pub", "bar ", "venue"), "hospitality"),
    (("physio", "chiropractor", "osteopath", "wellness", "naturopath", "health clinic"), "health"),
    (("ecommerce", "ecom", "e-commerce", "shopify", "online store"), "ecom"),
    (("saas", "software platform", "b2b software"), "saas"),
    (("coach", "coaching", "mentor"), "coaching"),
    (("legal", "law firm", "lawyer", "solicitor", "barrister"), "legal"),
    (("marketing agency", "ai automation", "ai consulting", "growth agency"), "marketing-agency"),
    (("b2b ", "enterprise services"), "b2b-services"),
    (("local service", "local business", "service area"), "b2c-local"),
]


def industry_from_baseline() -> str:
    f = STATE / "business-baseline.md"
    if not f.is_file():
        return "default"
    text = f.read_text().lower()
    for keywords, industry in INDUSTRY_RULES:
        if any(k in text for k in keywords):
            return industry
    return "default"


def main():
    industry = industry_from_baseline()
    template = TEMPLATES / f"{industry}.json"
    if not template.is_file():
        template = TEMPLATES / "default.json"
    if not template.is_file():
        sys.stderr.write(f"[fail] no lifecycle template found at {template}\n")
        sys.exit(1)

    plan = json.loads(template.read_text())
    out = STATE / "lifecycle"
    out.mkdir(exist_ok=True)
    (out / "deploy-plan.json").write_text(json.dumps({
        "industry_detected": industry,
        "template_used": str(template.relative_to(SKILL)),
        "plan": plan,
        "status": "drafted",
        "next": "Owner reviews drafts in ~/marketing/calendar/draft-posts/lifecycle/, then runs delegate-email-drip + delegate-sms-instant agents to push to GHL/ManyChat as DRAFT.",
    }, indent=2))

    print(f"[ok] industry: {industry}")
    print(f"[ok] template: {template}")
    print(f"[ok] plan written to {out / 'deploy-plan.json'}")
    print()
    print("Next: ask Claude to invoke `delegate-email-drip` + `delegate-sms-instant` agents")
    print("      with this deploy-plan.json as context. They will generate voice-graded")
    print("      copy + push to GHL/ManyChat as DRAFT.")


if __name__ == "__main__":
    main()
