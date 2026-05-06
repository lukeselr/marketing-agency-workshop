#!/usr/bin/env python3
"""Instagram public profile scrape. Bio + follower count via the public profile HTML.

FREE: instagram.com/<handle>/ serves OG meta + a JSON blob in the HTML.
For deep data (post captions, recent media), the orchestrator should fall back to Playwright
with a logged-in session.
"""

from __future__ import annotations

import json
import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def find_handle(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' site:instagram.com')}"
    status, body = safe_get(url, timeout=10)
    if status != 200:
        return None
    m = re.search(r'instagram\.com/([a-z0-9_.]+)/?["\']', body, re.I)
    if m:
        h = m.group(1)
        if h.lower() not in {"p", "explore", "reel", "reels", "stories", "tv"}:
            return h
    return None


def parse_profile_html(html: str) -> dict:
    out: dict = {}
    m = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if m:
        desc = m.group(1)
        out["og_description"] = desc
        fol = re.search(r'([\d.,]+[KkMm]?)\s+Followers', desc)
        if fol:
            out["followers_text"] = fol.group(1)
            out["followers"] = parse_count(fol.group(1))
        bio_match = re.search(r'-\s*([^"-][^"]+)$', desc)
        if bio_match:
            out["bio"] = bio_match.group(1).strip()
    m = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    if m:
        out["og_title"] = m.group(1)
    return out


def parse_count(s: str) -> int:
    s = s.strip().replace(",", "")
    mult = 1
    if s.endswith(("K", "k")):
        mult = 1_000
        s = s[:-1]
    elif s.endswith(("M", "m")):
        mult = 1_000_000
        s = s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "instagram-public", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace(" ", "").lower()
    direct_url = f"https://www.instagram.com/{base}/"
    status, body = safe_get(direct_url, timeout=12)

    handle = base
    if status != 200 or "Sorry, this page isn" in body or "Page Not Found" in body:
        handle = find_handle(candidate.split(".")[0])
        if handle:
            direct_url = f"https://www.instagram.com/{handle}/"
            status, body = safe_get(direct_url, timeout=12)

    parsed: dict = {}
    if status == 200 and body:
        parsed = parse_profile_html(body)

    emit({
        "scraper": "instagram-public",
        "status": "ok" if parsed else "no_profile",
        "input": inp,
        "profile_url": direct_url,
        "handle": handle,
        "bio": parsed.get("bio"),
        "followers": parsed.get("followers"),
        "followers_text": parsed.get("followers_text"),
        "og_description": parsed.get("og_description"),
        "needs_playwright_for_posts": True,
    })


if __name__ == "__main__":
    main()
