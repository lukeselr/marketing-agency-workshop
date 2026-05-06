#!/usr/bin/env python3
"""Free web search via DuckDuckGo HTML endpoint. Returns top organic results.

FREE: html.duckduckgo.com is unauth, returns parseable HTML.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def ddg_search(query: str, max_results: int = 15) -> list[dict]:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    status, body = safe_get(url, timeout=15, headers={"Accept": "text/html"})
    if status != 200 or not body:
        return []

    results: list[dict] = []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(body, "html.parser")
        for a in soup.select("a.result__a")[:max_results]:
            href = a.get("href") or ""
            title = a.get_text(strip=True)
            snippet_el = a.find_parent("div", class_=re.compile("result")) if a else None
            snippet = ""
            if snippet_el:
                sn = snippet_el.select_one(".result__snippet")
                if sn:
                    snippet = sn.get_text(" ", strip=True)
            if href and title:
                results.append({"url": href, "title": title, "snippet": snippet[:300]})
    except Exception:
        for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', body):
            results.append({"url": m.group(1), "title": m.group(2).strip(), "snippet": ""})
            if len(results) >= max_results:
                break
    return results


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "google-search", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    queries = [
        base,
        f"{base} reviews",
        f"{base} press",
        f"{base} pricing",
    ]
    if inp.get("city"):
        queries.append(f"{base} {inp['city']}")

    found: dict[str, dict] = {}
    for q in queries:
        for r in ddg_search(q, 10):
            found.setdefault(r["url"], r)

    emit({
        "scraper": "google-search",
        "status": "ok" if found else "no_results",
        "input": inp,
        "queries": queries,
        "result_count": len(found),
        "results": list(found.values())[:30],
    })


if __name__ == "__main__":
    main()
