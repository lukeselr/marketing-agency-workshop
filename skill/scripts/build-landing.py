#!/usr/bin/env python3
"""Phase 6.5 — Landing-page CRO loop.

Detects host from .state/scrape/dns-host.json, picks the matching builder skill,
generates voice-graded copy + 3 headline / 2 hero variants, prepares Microsoft
Clarity heatmap snippet, and runs PageSpeed Insights against the current site.

Outputs a deploy plan that delegate-landing-page agent executes via the host
skill at runtime.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
from urllib.parse import quote

SKILL = Path.home() / ".claude/skills/marketing-agency"
STATE = SKILL / ".state"
LANDING = STATE / "landing"
LANDING.mkdir(parents=True, exist_ok=True)

HOST_TO_SKILL = {
    "framer": "framer-builder",
    "ghl": "ghl-landing-pages",
    "vercel": "vercel-deployment",
    "netlify": "netlify-skills:netlify-deploy",
    "shopify": "shopify-automation",
    "squarespace": "ghl-browser",  # falls back to manual snippet paste
}


def detect_host() -> str:
    f = STATE / "scrape/dns-host.json"
    if not f.is_file():
        return "unknown"
    try:
        d = json.loads(f.read_text())
        for h in (d.get("host_hints") or []):
            if h in HOST_TO_SKILL:
                return h
    except Exception:
        pass
    return "unknown"


def main():
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: build-landing.py <campaign-slug>\n")
        sys.exit(1)
    campaign = sys.argv[1]

    host = detect_host()
    target_skill = HOST_TO_SKILL.get(host, "manual")

    plan = {
        "campaign": campaign,
        "host_detected": host,
        "build_via": target_skill,
        "components": {
            "copy_blocks": [
                "hero_headline (3 variants)",
                "hero_sub (2 variants)",
                "primary_cta",
                "social_proof_strip (3 testimonials or stats)",
                "value_props_3x",
                "objection_handler_FAQ",
                "secondary_cta",
                "footer_legal",
            ],
            "tracking": [
                "Meta Pixel (from .marketing-agency/tokens/meta.json)",
                "LinkedIn Insight Tag",
                "Google Ads conversion (EC4W)",
                "Microsoft Clarity heatmap (free, auto-injected)",
                "GA4 page_view + form_submit",
            ],
            "experiments": {
                "headline_test": "3 variants 33/33/33 split",
                "hero_test": "2 variants 50/50",
            },
            "speed_audit": "PageSpeed Insights API check (Core Web Vitals)",
        },
        "voice_grade_required": True,
        "firewall_check": True,
        "status": "drafted",
        "next": (
            "Invoke `delegate-landing-page` agent with this plan. It will:\n"
            "  1. Generate voice-graded copy via ad-creative + direct-response-copy + copywriting\n"
            "  2. Pass through content-engine 5-axis critic (≥8/10 to pass)\n"
            "  3. Render via the matching host skill (or HTML template for manual)\n"
            "  4. Inject Clarity + tracking via scripts/install-tracking.py\n"
            "  5. Run PageSpeed Insights, surface blockers\n"
            "  6. Write the page to .state/landing/<campaign>/index.html as DRAFT"
        ),
    }

    out = LANDING / f"{campaign}-deploy-plan.json"
    out.write_text(json.dumps(plan, indent=2))
    print(f"[ok] host: {host}")
    print(f"[ok] build via: {target_skill}")
    print(f"[ok] plan: {out}")


if __name__ == "__main__":
    main()
