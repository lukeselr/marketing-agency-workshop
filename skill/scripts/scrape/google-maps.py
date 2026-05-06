#!/usr/bin/env python3
"""Google Maps / GMB lookup. Two-pass: DuckDuckGo to find the GMB URL, then HTML scrape it.

FREE: no Google API key. Uses DDG to find GMB URL, then plain GET on maps.google.com.
Many fields require Playwright with JS — this returns whatever shows up in the static HTML.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def find_maps_url(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' site:google.com/maps')}"
    status, body = safe_get(url, timeout=12)
    if status != 200:
        return None
    m = re.search(r'href="(https?://(?:www\.)?google\.[^/]+/maps/[^"]+)"', body)
    return m.group(1) if m else None


def parse_maps_excerpt(html: str) -> dict:
    out: dict = {}
    rating = re.search(r'(\d\.\d)\s*(?:stars?|out of)', html, re.I)
    review_count = re.search(r'(\d{1,3}(?:[, ]\d{3})*)\s*review', html, re.I)
    address = re.search(r'"address":\s*"([^"]+)"', html)
    if rating:
        try:
            out["rating"] = float(rating.group(1))
        except ValueError:
            pass
    if review_count:
        try:
            out["review_count"] = int(re.sub(r"[^\d]", "", review_count.group(1)))
        except ValueError:
            pass
    if address:
        out["address"] = address.group(1)
    return out


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "google-maps", "status": "skipped", "reason": "no name/domain"})
        return

    base_query = candidate.split(".")[0].replace("-", " ")
    if inp.get("city"):
        base_query = f"{base_query} {inp['city']}"

    maps_url = find_maps_url(base_query)
    extracted: dict = {}
    if maps_url:
        status, body = safe_get(maps_url, timeout=15)
        if status == 200 and body:
            extracted = parse_maps_excerpt(body)

    emit({
        "scraper": "google-maps",
        "status": "ok" if maps_url else "no_listing_found",
        "input": inp,
        "query": base_query,
        "maps_url": maps_url,
        "rating": extracted.get("rating"),
        "review_count": extracted.get("review_count"),
        "address": extracted.get("address"),
        "needs_playwright_for_full_data": True,
    })


if __name__ == "__main__":
    main()
