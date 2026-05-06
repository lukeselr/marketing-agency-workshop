#!/usr/bin/env python3
"""Aggregate reviews across Trustpilot, ProductReview AU, Google (via google-maps), Yelp.

FREE: scrapes public review pages via DDG-find + GET. Returns combined count + avg rating.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


SOURCES = [
    ("trustpilot", "site:trustpilot.com"),
    ("productreview_au", "site:productreview.com.au"),
    ("yelp_au", "site:yelp.com.au"),
    ("google_business", "site:google.com/maps"),
]


def find_url(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    status, body = safe_get(url, timeout=10)
    if status != 200:
        return None
    m = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', body)
    return m.group(1) if m else None


def parse_listing(html: str) -> tuple[int | None, float | None]:
    count = None
    rating = None
    rc = re.search(r'(\d{1,3}(?:[, ]\d{3})*)\s*review', html, re.I)
    if rc:
        try:
            count = int(re.sub(r"[^\d]", "", rc.group(1)))
        except ValueError:
            pass
    rt = re.search(r'(\d\.\d)\s*(?:stars?|out of|/\s*5)', html, re.I)
    if rt:
        try:
            rating = float(rt.group(1))
        except ValueError:
            pass
    return count, rating


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "reviews", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    per_source: dict[str, dict] = {}
    total_count = 0
    rating_samples: list[float] = []

    for key, op in SOURCES:
        listing_url = find_url(f"{base} {op}")
        per: dict = {"listing_url": listing_url}
        if listing_url:
            status, body = safe_get(listing_url, timeout=12)
            if status == 200 and body:
                count, rating = parse_listing(body)
                per["count"] = count
                per["rating"] = rating
                if count:
                    total_count += count
                if rating:
                    rating_samples.append(rating)
        per_source[key] = per

    avg = (sum(rating_samples) / len(rating_samples)) if rating_samples else None

    emit({
        "scraper": "reviews",
        "status": "ok" if per_source else "no_data",
        "input": inp,
        "sources": per_source,
        "count": total_count or None,
        "avg_rating": round(avg, 2) if avg is not None else None,
    })


if __name__ == "__main__":
    main()
