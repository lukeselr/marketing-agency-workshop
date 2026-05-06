#!/usr/bin/env python3
"""Merge Phase 1 scraper outputs into a scannable business-baseline.md.

Designed for the user's first read. Six expandable cards, each lead with the
single-most-useful fact, hide noise, and end with a clear "what to confirm"
section. The LLM in Claude Code shows this back to the user, asks for edits,
then proceeds to the 5 private questions.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_scrapes(scrape_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in sorted(scrape_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text())
            name = data.get("scraper", f.stem)
            out[name] = data
        except Exception as exc:
            out[f.stem] = {"scraper": f.stem, "status": "parse_error", "error": str(exc)}
    return out


def first_truthy(*vals):
    for v in vals:
        if v:
            return v
    return None


def country_from_tld(domain: str | None) -> str | None:
    if not domain:
        return None
    tld_map = {
        ".au": "Australia", ".com.au": "Australia",
        ".nz": "New Zealand", ".co.nz": "New Zealand",
        ".uk": "United Kingdom", ".co.uk": "United Kingdom",
        ".ca": "Canada",
        ".us": "United States",
    }
    for tld, country in sorted(tld_map.items(), key=lambda x: -len(x[0])):
        if domain.endswith(tld):
            return country
    return None


def extract_name(web: dict) -> str | None:
    """Pull the business name from the homepage <title> or og:site_name."""
    pages = web.get("pages") or []
    home = next((p for p in pages if p.get("path") == "/"), pages[0] if pages else {})
    meta = home.get("meta") or {}
    og_site = meta.get("meta:og:site_name") or meta.get("meta:og:title")
    title = meta.get("title") or ""
    if og_site:
        return og_site.strip()
    if title:
        # "Selr AI · We install AI systems" → "Selr AI"
        for sep in [" · ", " | ", " - ", " — ", ": "]:
            if sep in title:
                return title.split(sep, 1)[0].strip()
        return title.strip()[:60]
    return None


def host_label(dns: dict, web: dict) -> str | None:
    hints = dns.get("host_hints") or []
    if not hints:
        return None
    label_map = {
        "framer": "Framer",
        "vercel": "Vercel / Next.js",
        "netlify": "Netlify",
        "shopify": "Shopify",
        "squarespace": "Squarespace",
        "wix": "Wix",
        "cloudflare-cdn": "Cloudflare (CDN only — origin host below)",
        "ghl": "GoHighLevel",
        "google-workspace-email": "Google Workspace email",
        "microsoft-365-email": "Microsoft 365 email",
    }
    site = [h for h in hints if h not in {"google-workspace-email", "microsoft-365-email"}]
    email = [h for h in hints if h in {"google-workspace-email", "microsoft-365-email"}]
    parts = []
    if site:
        parts.append("Site: " + ", ".join(label_map.get(h, h) for h in site))
    if email:
        parts.append("Email: " + ", ".join(label_map.get(h, h) for h in email))
    return " · ".join(parts) if parts else None


def classify_industry(web: dict) -> str | None:
    """Lightweight keyword classification from website text."""
    pages = web.get("pages") or []
    text = " ".join(p.get("text_excerpt", "") for p in pages).lower()
    if not text:
        return None
    rules = [
        ("AI / automation consulting", ["ai automation", "automate your business", "ai consulting", "build ai systems"]),
        ("Real estate", ["realestate", "buy a home", "list your property", "real estate agent"]),
        ("Trades / construction", ["plumbing", "electrician", "builder", "renovation", "carpentry"]),
        ("Hospitality / restaurant", ["dine", "menu", "reservation", "book a table"]),
        ("Health / wellness", ["chiropractor", "physio", "wellness", "personal training"]),
        ("E-commerce", ["add to cart", "shop now", "free shipping", "size guide"]),
        ("SaaS / software", ["pricing per user", "free trial", "api docs", "developer docs"]),
        ("Marketing agency", ["full-service agency", "scale your business", "growth marketing"]),
        ("Coaching / consulting", ["1:1 coaching", "book a strategy call", "mentorship"]),
        ("Legal", ["solicitor", "barrister", "law firm"]),
    ]
    for label, kws in rules:
        if any(k in text for k in kws):
            return label
    return None


def card(num: int, title: str, lines: list[str]) -> str:
    body = "\n".join(f"- {l}" for l in lines if l)
    if not body:
        body = "- _(none detected — confirm with the user if relevant)_"
    return f"## {num}. {title}\n\n{body}\n\n"


def render(scrapes: dict[str, dict], raw_input: str) -> str:
    web = scrapes.get("website", {})
    dns = scrapes.get("dns-host", {})
    abn = scrapes.get("abn-lookup", {})
    gmaps = scrapes.get("google-maps", {})
    li_page = scrapes.get("linkedin-page", {})
    ig = scrapes.get("instagram-public", {})
    fb_page = scrapes.get("facebook-page", {})
    meta_ads = scrapes.get("meta-ad-library", {})
    li_ads = scrapes.get("linkedin-ad-library", {})
    g_ads = scrapes.get("google-ads-transparency", {})
    reviews = scrapes.get("reviews", {})
    news = scrapes.get("news-mentions", {})
    industry_dirs = scrapes.get("industry-directories", {})
    google_search = scrapes.get("google-search", {})

    domain = web.get("domain") or dns.get("domain")
    name = first_truthy(
        abn.get("entity_name"),
        extract_name(web),
        li_page.get("title", "").split(" |")[0].strip() if li_page.get("title") else None,
        domain,
    )
    industry = classify_industry(web)
    country = country_from_tld(domain)
    age_signal = web.get("wayback_snapshots") or 0
    age_text = (
        f"~{age_signal} Wayback snapshots (rough age signal)"
        if age_signal else "Wayback unknown — likely recent or low traffic"
    )
    pixels = list((web.get("tracking_pixels_detected") or {}).keys())

    out: list[str] = []
    out.append(f"# Business Baseline: {name or domain or raw_input}\n\n")
    out.append(f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_\n\n")
    out.append(f"_Auto-discovered from 14 free public sources in ~15 sec. "
               f"Review each card. Reply with corrections or 'looks good'._\n\n---\n\n")

    # Card 1 — Identity
    identity_lines = [
        f"**Name**: {name}" if name else None,
        f"**Domain**: {domain}",
        f"**Country**: {country}" if country else None,
        f"**ABN**: {abn.get('abn')} ({abn.get('entity_type') or 'entity type unknown'})" if abn.get("abn") else None,
        f"**Trading age**: {age_text}",
    ]
    out.append(card(1, "Identity", [l for l in identity_lines if l]))

    # Card 2 — Tech stack
    tech_lines = [
        host_label(dns, web),
        f"**Tracking pixels detected**: {', '.join(pixels)}" if pixels else "**Tracking pixels detected**: none yet — Phase 6 will install",
        f"**Wayback snapshots**: {age_signal}" if age_signal else None,
    ]
    out.append(card(2, "Tech stack", [l for l in tech_lines if l]))

    # Card 3 — Online presence
    presence_lines = [
        f"**LinkedIn**: {li_page.get('followers')} followers · {li_page.get('employees_visible')} employees visible · `{li_page.get('company_url')}`"
        if li_page.get("followers") or li_page.get("employees_visible") else "**LinkedIn**: page not found or auth-walled",
        f"**Instagram**: {ig.get('followers')} followers · `{ig.get('profile_url')}`"
        if ig.get("followers") else "**Instagram**: profile not found from public scrape",
        f"**Facebook**: {fb_page.get('likes')} likes · `{fb_page.get('page_url')}`"
        if fb_page.get("likes") else "**Facebook**: page not found from public scrape",
        f"**Google Maps**: {gmaps.get('rating')}★ ({gmaps.get('review_count')} reviews)"
        if gmaps.get("rating") else None,
        f"**Industry directories** with hits: {industry_dirs.get('directory_count_with_hits') or 0}",
    ]
    out.append(card(3, "Online presence", [l for l in presence_lines if l]))

    # Card 4 — Active advertising
    def fmt_count(d: dict) -> str:
        c = d.get("ad_count")
        if c is None:
            return "needs Playwright auth scrape"
        return f"{c} ads detected"
    ads_lines = [
        f"**Meta Ad Library**: {fmt_count(meta_ads)}",
        f"**LinkedIn Ad Library**: {fmt_count(li_ads)}",
        f"**Google Ads Transparency**: {fmt_count(g_ads)}",
    ]
    out.append(card(4, "Active advertising", ads_lines))

    # Card 5 — Reputation + press
    rep_lines = [
        f"**Aggregated reviews**: {reviews.get('count') or 0} (avg {reviews.get('avg_rating') or 'n/a'}★)",
        f"**News mentions (last 12mo)**: {news.get('count') or 0}",
        f"**Public search hits**: {google_search.get('result_count') or 0}",
    ]
    out.append(card(5, "Reputation + press", rep_lines))

    # Card 6 — Industry + sub-niche guess
    niche_lines = [
        f"**Industry guess**: {industry}" if industry else "**Industry guess**: unclear from site copy — please confirm",
        f"**Pages crawled**: {web.get('pages_found') or 0}",
    ]
    pages_found = web.get("pages") or []
    if pages_found:
        for p in pages_found[:6]:
            title = (p.get("meta") or {}).get("title", "(untitled)")
            niche_lines.append(f"  · `{p['path']}` — {title}")
    out.append(card(6, "Industry + content", niche_lines))

    # What we couldn't find
    missing = []
    if not abn.get("abn"):
        missing.append("ABN / business registration")
    if not (gmaps.get("rating") or reviews.get("count")):
        missing.append("review aggregator listing")
    if not (li_page.get("followers") or ig.get("followers")):
        missing.append("major social presence")
    if not industry:
        missing.append("clear industry signal from website copy")
    if missing:
        out.append("## What we could not auto-detect\n\n")
        for m in missing:
            out.append(f"- {m}\n")
        out.append("\n_If any of these matter, paste them in your reply._\n\n")

    # Scraper status
    out.append("---\n\n## Scraper status (debug)\n\n")
    out.append("| Scraper | Status |\n|---|---|\n")
    for sc, data in sorted(scrapes.items()):
        out.append(f"| {sc} | {data.get('status', '?')} |\n")
    out.append("\n")
    out.append("---\n\n")
    out.append("## Next: 5 lean questions (the only things public data can not give us)\n\n")
    out.append("1. **Monthly ad budget** you're comfortable spending?\n")
    out.append("2. **Most painful bottleneck** in your business right now?\n")
    out.append("3. Any of the auto-detected names above that's a real competitor (1-2)?\n")
    out.append("4. Comfort 1-5 per platform (Meta / Google / LinkedIn).\n")
    out.append("5. Existing ad accounts to connect, or all-new?\n")
    out.append("\nRun `bash scripts/ask-questions.sh` to capture answers, or reply inline.\n")
    return "".join(out)


def main() -> None:
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: synthesize.py <scrape_dir> [raw_input]\n")
        sys.exit(1)
    scrape_dir = Path(sys.argv[1])
    raw = sys.argv[2] if len(sys.argv) > 2 else ""
    if not scrape_dir.is_dir():
        sys.stderr.write(f"Not a directory: {scrape_dir}\n")
        sys.exit(1)
    scrapes = load_scrapes(scrape_dir)
    sys.stdout.write(render(scrapes, raw))


if __name__ == "__main__":
    main()
