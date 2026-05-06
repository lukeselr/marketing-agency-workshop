#!/usr/bin/env python3
"""Phase 6 — install Pixel + Insight Tag + Google Ads conversion tracking.

Detects host (Framer / Vercel / GHL / Webflow / WordPress / Shopify / Squarespace / GTM)
from the dns-host scraper output, then emits an injection recipe per host.

This script does NOT auto-edit the live site (host-dependent + risky). It writes a
per-host install plan to .state/tracking-plan.md plus the exact tag snippets, and the
parent skill drives the install via the appropriate sub-skill (framer-builder, ghl-landing-pages, etc).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


SKILL_DIR = Path.home() / ".claude/skills/marketing-agency"
STATE_DIR = SKILL_DIR / ".state"
TOKENS_DIR = Path.home() / ".marketing-agency/tokens"


def load_json(p: Path) -> dict:
    if p.is_file():
        try:
            return json.loads(p.read_text())
        except Exception:
            return {}
    return {}


def detect_host() -> str:
    dns = load_json(STATE_DIR / "scrape" / "dns-host.json")
    hints = dns.get("host_hints") or []
    for known in ("framer", "vercel", "netlify", "shopify", "ghl"):
        if known in hints:
            return known
    return "unknown"


def meta_pixel_snippet(pixel_id: str) -> str:
    return f"""<!-- Meta Pixel -->
<script>
!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;
n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,
document,'script','https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel_id}');
fbq('track', 'PageView');
</script>
<noscript><img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"/></noscript>
<!-- End Meta Pixel -->"""


def linkedin_snippet(partner_id: str) -> str:
    return f"""<!-- LinkedIn Insight Tag -->
<script type="text/javascript">
_linkedin_partner_id = "{partner_id}";
window._linkedin_data_partner_ids = window._linkedin_data_partner_ids || [];
window._linkedin_data_partner_ids.push(_linkedin_partner_id);
</script>
<script type="text/javascript">
(function(l) {{
if (!l){{window.lintrk = function(a,b){{window.lintrk.q.push([a,b])}}; window.lintrk.q=[]}}
var s = document.getElementsByTagName("script")[0];
var b = document.createElement("script");
b.type = "text/javascript";b.async = true;
b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
s.parentNode.insertBefore(b, s);}})(window.lintrk);
</script>
<noscript><img height="1" width="1" style="display:none;" alt=""
src="https://px.ads.linkedin.com/collect/?pid={partner_id}&fmt=gif" /></noscript>
<!-- End LinkedIn Insight Tag -->"""


def google_ads_snippet(conversion_id: str, conversion_label: str) -> str:
    return f"""<!-- Google Ads Conversion -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-{conversion_id}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'AW-{conversion_id}');
</script>
<!-- Conversion event helper:
gtag('event', 'conversion', {{ 'send_to': 'AW-{conversion_id}/{conversion_label}' }});
-->
<!-- End Google Ads Conversion -->"""


def main() -> None:
    host = detect_host()
    meta = load_json(TOKENS_DIR / "meta.json")
    li = load_json(TOKENS_DIR / "linkedin.json")
    g = load_json(TOKENS_DIR / "google-ads.json")

    plan = ["# Tracking install plan", "", f"_Detected host: **{host}**_", ""]

    snippets: list[tuple[str, str]] = []
    if meta.get("pixel_id"):
        snippets.append(("meta_pixel", meta_pixel_snippet(meta["pixel_id"])))
    if li.get("insight_tag_partner_id"):
        snippets.append(("linkedin_insight", linkedin_snippet(li["insight_tag_partner_id"])))
    if g.get("conversion_action_id_purchase"):
        snippets.append(("google_ads", google_ads_snippet(g["conversion_action_id_purchase"], "PURCHASE_LABEL")))

    if not snippets:
        plan.append("No tokens found yet. Run Phase 3 + Phase 4 first.\n")
    else:
        plan.append("## Snippets to inject (head)\n")
        for name, snippet in snippets:
            plan.append(f"### {name}\n\n```html\n{snippet}\n```\n")

    plan.append("## Per-host install path\n")
    plan.append({
        "framer": "Use `framer-builder` skill — `Site Settings → Site → Custom Code → End of <head>`.",
        "ghl": "Use `ghl-landing-pages` skill — Funnel/Page → Settings → Tracking & Analytics.",
        "vercel": "Edit your Next.js layout — add to `<head>` in `app/layout.tsx`. Redeploy.",
        "netlify": "Edit site → `_app.js` or `_document.js` head. Redeploy.",
        "shopify": "Online Store → Themes → Edit code → `theme.liquid` → before `</head>`.",
        "unknown": "Manual: paste into the site's `<head>` via your CMS or build pipeline.",
    }[host if host in {"framer", "ghl", "vercel", "netlify", "shopify"} else "unknown"])
    plan.append("")
    plan.append("## Verification\n")
    plan.append("After install:\n")
    plan.append("- Meta Pixel: `events_manager2/pixels/<pixel_id>/test_events` shows hits.\n")
    plan.append("- LinkedIn: campaignmanager → Insight Tag → status `Active`.\n")
    plan.append("- Google Ads: Tag Assistant Chrome extension shows green status on the site.\n")

    out = STATE_DIR / "tracking-plan.md"
    out.write_text("\n".join(plan))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
