#!/usr/bin/env python3
"""LinkedIn Ad Library lookup. Public-search URL emit + count attempt.

FREE: linkedin.com/ad-library/search is public, but most data is JS-rendered.
The orchestrator must use Playwright with the user's session for full ad copy.
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
        emit({"scraper": "linkedin-ad-library", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    search_url = f"https://www.linkedin.com/ad-library/search?keywords={quote_plus(base)}"

    status, body = safe_get(search_url, timeout=15)

    ad_count = None
    if status == 200 and body:
        m = re.search(r'(\d+)\s*ads?\s*(?:found|matching)', body, re.I)
        if m:
            try:
                ad_count = int(m.group(1))
            except ValueError:
                pass

    emit({
        "scraper": "linkedin-ad-library",
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
