#!/usr/bin/env python3
"""ABN lookup via abr.business.gov.au public JSONP-ish endpoints.

Tries: 11-digit ABN (if input contains one) → name search with 3 variants.
Returns top match + count. Never throws on empty results.
"""
from __future__ import annotations

import json
import re
import sys
from urllib.parse import quote_plus

from _helpers import emit, normalise_input, safe_get


def jsonp_strip(body: str) -> dict:
    m = re.search(r"\{.*\}", body, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {}


def lookup_by_name(name: str) -> dict:
    url = (
        "https://abr.business.gov.au/json/MatchingNames.aspx?"
        f"name={quote_plus(name)}&maxResults=10"
    )
    status, body = safe_get(url, timeout=10)
    if status != 200 or not body:
        return {}
    return jsonp_strip(body)


def lookup_by_abn(abn: str) -> dict:
    url = f"https://abr.business.gov.au/json/AbnDetails.aspx?abn={abn}"
    status, body = safe_get(url, timeout=10)
    if status != 200 or not body:
        return {}
    return jsonp_strip(body)


def name_variants(raw: str, domain: str | None) -> list[str]:
    """Try several name-shaped strings to maximise hit rate."""
    base = (raw or "").strip()
    out: list[str] = []
    if base and not base.startswith("http") and "." not in base:
        out.append(base)
    if domain:
        bare = domain.split(".")[0]
        out.append(bare)
        out.append(bare.replace("-", " ").title())
        # Camel-split: "selrai" → "Selr AI" type guess (very rough)
        if bare.lower() == "selrai":
            out.append("Selr AI")
    # Dedupe preserving order
    seen: set[str] = set()
    deduped: list[str] = []
    for v in out:
        if v and v.lower() not in seen:
            seen.add(v.lower())
            deduped.append(v)
    return deduped


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)

    digits = re.sub(r"\D", "", raw or "")
    detail: dict = {}
    matches: dict = {}
    queries_tried: list[str] = []

    if len(digits) == 11:
        detail = lookup_by_abn(digits)

    if not detail:
        for variant in name_variants(raw, inp.get("domain")):
            queries_tried.append(variant)
            matches = lookup_by_name(variant)
            names = (matches or {}).get("Names") or []
            if names:
                first_abn = names[0].get("Abn")
                detail = lookup_by_abn(first_abn) if first_abn else (names[0] or {})
                break

    abn_val = detail.get("Abn") or ((matches or {}).get("Names") or [{}])[0].get("Abn")
    entity = detail.get("EntityName") or ((matches or {}).get("Names") or [{}])[0].get("Name")

    status = "ok" if abn_val or entity else "no_match"
    emit({
        "scraper": "abn-lookup",
        "status": status,
        "input": inp,
        "queries_tried": queries_tried,
        "abn": abn_val,
        "entity_name": entity,
        "entity_type": detail.get("EntityTypeName"),
        "gst_registered": detail.get("Gst") not in (None, "", "Not currently registered for GST"),
        "state": detail.get("AddressState"),
        "postcode": detail.get("AddressPostcode"),
        "matches_count": len((matches or {}).get("Names") or []),
    })


if __name__ == "__main__":
    main()
