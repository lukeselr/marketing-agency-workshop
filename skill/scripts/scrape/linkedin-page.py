#!/usr/bin/env python3
"""LinkedIn company page surface scrape. Most data is auth-walled; this returns OG meta + signal flags.

FREE: linkedin.com/company/<slug> serves limited OG meta to unauth requests.
For deep data, the orchestrator should fall back to a Playwright session with the user's cookies.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, extract_meta, normalise_input, safe_get


def find_company_slug(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query + ' site:linkedin.com/company')}"
    status, body = safe_get(url, timeout=10)
    if status != 200:
        return None
    m = re.search(r'linkedin\.com/company/([a-z0-9\-]+)', body, re.I)
    return m.group(1) if m else None


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "linkedin-page", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace(" ", "-").lower()
    direct_url = f"https://www.linkedin.com/company/{base}/"
    status, body = safe_get(direct_url, timeout=12)

    slug = base
    if status != 200 or not body or "Page not found" in body:
        slug = find_company_slug(candidate.split(".")[0])
        if slug:
            direct_url = f"https://www.linkedin.com/company/{slug}/"
            status, body = safe_get(direct_url, timeout=12)

    meta: dict = {}
    description = ""
    if status == 200 and body:
        meta = extract_meta(body)
        m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', body)
        if m:
            description = m.group(1)

    follower_match = re.search(r'(\d{1,3}(?:[, ]\d{3})*)\s+followers', (body or ""), re.I)
    employee_match = re.search(r'(\d+)\s*(?:employees|associated members)', (body or ""), re.I)

    emit({
        "scraper": "linkedin-page",
        "status": "ok" if status == 200 else "no_page",
        "input": inp,
        "company_url": direct_url,
        "slug": slug,
        "title": meta.get("title"),
        "description": description[:500],
        "followers": int(re.sub(r"[^\d]", "", follower_match.group(1))) if follower_match else None,
        "employees_visible": int(employee_match.group(1)) if employee_match else None,
        "needs_playwright_for_posts": True,
    })


if __name__ == "__main__":
    main()
