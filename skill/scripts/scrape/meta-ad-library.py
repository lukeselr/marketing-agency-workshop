#!/usr/bin/env python3
"""Meta Ad Library lookup. Public-search URL emit + lightweight count attempt.

FREE: facebook.com/ads/library is public, but the count + ad copy are JS-rendered.
This script emits the search URL + tries a static count via DDG indexed snippet.
For full ad copy + media, the orchestrator must follow up with Playwright.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "meta-ad-library", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    search_url = (
        "https://www.facebook.com/ads/library/?"
        "active_status=all&ad_type=all&country=AU&"
        f"q={quote_plus(base)}&search_type=keyword_unordered"
    )

    status, body = safe_get(search_url, timeout=15)

    ad_count = None
    if status == 200 and body:
        m = re.search(r'"total_count"\s*:\s*(\d+)', body)
        if m:
            try:
                ad_count = int(m.group(1))
            except ValueError:
                pass
        if ad_count is None:
            m2 = re.search(r'(\d+)\s+results?', body, re.I)
            if m2:
                try:
                    ad_count = int(m2.group(1))
                except ValueError:
                    pass

    emit({
        "scraper": "meta-ad-library",
        "status": "ok",
        "input": inp,
        "search_url": search_url,
        "query": base,
        "ad_count": ad_count,
        "playwright_required_for_full_data": True,
        "playwright_target_url": search_url,
    })


if __name__ == "__main__":
    main()
