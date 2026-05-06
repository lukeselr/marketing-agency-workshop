#!/usr/bin/env python3
"""Google Ads Transparency Center lookup. Public-search URL emit + count attempt.

FREE: adstransparency.google.com is public + indexable. Most data is JS-rendered, so this
emits the search URL so the orchestrator can follow up with Playwright.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["domain"] or inp["name"]
    if not candidate:
        emit({"scraper": "google-ads-transparency", "status": "skipped", "reason": "no domain/name"})
        return

    target_term = inp["domain"] or candidate.split(".")[0]
    search_url = (
        "https://adstransparency.google.com/?"
        f"region=AU&domain={quote_plus(target_term)}"
    )

    status, body = safe_get(search_url, timeout=15)
    ad_count = None
    if status == 200 and body:
        m = re.search(r'(\d+)\s+ads?', body, re.I)
        if m:
            try:
                ad_count = int(m.group(1))
            except ValueError:
                pass

    emit({
        "scraper": "google-ads-transparency",
        "status": "ok",
        "input": inp,
        "search_url": search_url,
        "query": target_term,
        "ad_count": ad_count,
        "playwright_required_for_full_data": True,
        "playwright_target_url": search_url,
    })


if __name__ == "__main__":
    main()
