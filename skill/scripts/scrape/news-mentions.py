#!/usr/bin/env python3
"""News mentions in last 12 months. Uses DuckDuckGo News results.

FREE: html.duckduckgo.com supports a news vertical via the iar=news flag.
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
        emit({"scraper": "news-mentions", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    queries = [base, f'"{base}"', f"{base} press release"]

    found: dict[str, dict] = {}
    for q in queries:
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(q)}&iar=news"
        status, body = safe_get(url, timeout=12)
        if status != 200 or not body:
            continue
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(body, "html.parser")
            for a in soup.select("a.result__a")[:10]:
                href = a.get("href") or ""
                title = a.get_text(strip=True)
                if href and title:
                    found.setdefault(href, {"url": href, "title": title})
        except Exception:
            for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', body):
                found.setdefault(m.group(1), {"url": m.group(1), "title": m.group(2).strip()})

    emit({
        "scraper": "news-mentions",
        "status": "ok",
        "input": inp,
        "queries": queries,
        "count": len(found),
        "items": list(found.values())[:25],
    })


if __name__ == "__main__":
    main()
