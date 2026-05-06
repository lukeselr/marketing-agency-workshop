#!/usr/bin/env python3
"""Probe AU industry directories for listings. Light HEAD-style check — does a listing exist?

FREE: just attempts predictable directory URL patterns + DDG search hits per directory.
"""

from __future__ import annotations

import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


DIRECTORIES = {
    "truelocal": "site:truelocal.com.au",
    "yellowpages_au": "site:yellowpages.com.au",
    "productreview": "site:productreview.com.au",
    "hipages": "site:hipages.com.au",
    "oneflare": "site:oneflare.com.au",
    "airtasker": "site:airtasker.com",
    "domain": "site:domain.com.au",
    "realestate_au": "site:realestate.com.au",
    "ratemyagent": "site:ratemyagent.com.au",
    "tripadvisor": "site:tripadvisor.com",
    "yelp": "site:yelp.com.au",
    "opentable": "site:opentable.com.au",
    "healthengine": "site:healthengine.com.au",
    "bookwell": "site:bookwell.com.au",
    "linkedin_company": "site:linkedin.com/company",
}


def ddg_first_hit(query: str) -> str | None:
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    status, body = safe_get(url, timeout=10)
    if status != 200:
        return None
    m = re.search(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', body)
    return m.group(1) if m else None


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    candidate = inp["name"] or inp["domain"]
    if not candidate:
        emit({"scraper": "industry-directories", "status": "skipped", "reason": "no name/domain"})
        return

    base = candidate.split(".")[0].replace("-", " ")
    listings: dict[str, str] = {}
    for key, site_op in DIRECTORIES.items():
        q = f"{base} {site_op}"
        hit = ddg_first_hit(q)
        if hit:
            listings[key] = hit

    emit({
        "scraper": "industry-directories",
        "status": "ok",
        "input": inp,
        "directories_with_hits": list(listings.keys()),
        "listings": listings,
        "directory_count_with_hits": len(listings),
    })


if __name__ == "__main__":
    main()
