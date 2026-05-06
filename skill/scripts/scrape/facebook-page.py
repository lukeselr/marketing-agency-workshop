#!/usr/bin/env python3
"""Facebook Page surface scrape. Page identity + likes-when-visible without auth.

FREE: facebook.com/<page>/ serves limited OG metadata to unauth requests; deeper data
(posts, ads attribution) requires Playwright with a logged-in session.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, extract_meta, normalise_input, safe_get


def find_page_slug(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' site:facebook.com')}"
    status, body = safe_get(url, timeout=10)
    if status != 200:
        return None
    m = re.search(r'facebook\.com/([A-Za-z0-9.\-]+)/?', body)
    if m:
        slug = m.group(1)
        if slug.lower() not in {"sharer", "tr", "watch", "events", "groups", "gaming"}:
            return slug
    return None


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "facebook-page", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace(" ", "").lower()
    direct_url = f"https://www.facebook.com/{base}/"
    status, body = safe_get(direct_url, timeout=12)

    slug = base
    if status != 200 or not body or "Page Not Found" in body:
        slug = find_page_slug(candidate.split(".")[0])
        if slug:
            direct_url = f"https://www.facebook.com/{slug}/"
            status, body = safe_get(direct_url, timeout=12)

    meta: dict = {}
    likes = None
    if status == 200 and body:
        meta = extract_meta(body)
        likes_match = re.search(r'(\d{1,3}(?:[, ]\d{3})*|\d+)\s*(?:people\s+like|likes)', body, re.I)
        if likes_match:
            try:
                likes = int(re.sub(r"[^\d]", "", likes_match.group(1)))
            except ValueError:
                pass

    emit({
        "scraper": "facebook-page",
        "status": "ok" if status == 200 else "no_page",
        "input": inp,
        "page_url": direct_url,
        "slug": slug,
        "title": meta.get("title"),
        "likes": likes,
        "needs_playwright_for_posts_and_ads": True,
    })


if __name__ == "__main__":
    main()
