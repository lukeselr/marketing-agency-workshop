#!/usr/bin/env python3
"""Crawl the user's website. Homepage + key sub-pages + Wayback snapshot count.

FREE: requests + bs4 + Wayback CDX API (free).
"""

from __future__ import annotations

import sys
from urllib.parse import urljoin

from _helpers import emit, extract_meta, normalise_input, safe_get, text_only


KEY_PATHS = [
    "/",
    "/about",
    "/about-us",
    "/services",
    "/pricing",
    "/contact",
    "/blog",
    "/case-studies",
    "/testimonials",
    "/work",
    "/portfolio",
]


def wayback_count(domain: str) -> int:
    """Count Wayback Machine snapshots for the domain (rough age + history signal)."""
    url = f"https://web.archive.org/cdx/search/cdx?url={domain}&output=json&limit=1&showResumeKey=false"
    status, body = safe_get(url, timeout=10)
    if status == 200 and body:
        # First line is header, count via newlines
        return max(0, body.count("\n") - 1)
    return 0


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    if not inp["url"] and not inp["domain"]:
        emit({"scraper": "website", "status": "skipped", "reason": "no domain"})
        return

    base = inp["url"] or f"https://{inp['domain']}"
    domain = inp["domain"] or base.replace("https://", "").replace("http://", "").split("/")[0]

    pages: list[dict] = []
    seen_titles: set[str] = set()

    for path in KEY_PATHS:
        url = urljoin(base, path)
        status, html = safe_get(url)
        if status != 200 or not html:
            continue
        meta = extract_meta(html)
        title = meta.get("title", "")
        if title in seen_titles:
            continue
        seen_titles.add(title)
        pages.append({
            "path": path,
            "status": status,
            "meta": meta,
            "text_excerpt": text_only(html, 5000),
        })

    snapshots = wayback_count(domain)

    # Cross-page tracking pixel detection
    pixels: dict[str, str] = {}
    for p in pages:
        for k, v in (p.get("meta") or {}).items():
            if k in {"meta_pixel", "ga4", "linkedin_insight", "google_ads", "tiktok_pixel"}:
                pixels[k] = v

    emit({
        "scraper": "website",
        "status": "ok",
        "input": inp,
        "domain": domain,
        "base_url": base,
        "pages_found": len(pages),
        "pages": pages,
        "wayback_snapshots": snapshots,
        "tracking_pixels_detected": pixels,
    })


if __name__ == "__main__":
    main()
