"""Shared helpers for marketing-agency Phase 1 scrapers.

Every scraper imports from here. Keeps the cost-stack pure FREE — only
stdlib + requests + beautifulsoup4. No paid SaaS.
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any
from urllib.parse import urlparse


def emit(payload: dict[str, Any]) -> None:
    """Write a single JSON payload to stdout (used by orchestrator to merge)."""
    json.dump(payload, sys.stdout, ensure_ascii=False, default=str)
    sys.stdout.write("\n")


def normalise_input(raw: str) -> dict[str, Any]:
    """Turn user input into structured business identifiers.

    Accepts:
      - https://example.com.au
      - example.com.au
      - "Acme Pty Ltd"
      - "Acme Pty Ltd Sydney"
    Returns: {"domain": str|None, "url": str|None, "name": str|None, "city": str|None}
    """
    s = (raw or "").strip()
    if not s:
        return {"domain": None, "url": None, "name": None, "city": None}

    looks_url = bool(re.search(r"\.[a-z]{2,}", s, re.I)) or s.startswith("http")
    if looks_url:
        url = s if s.startswith("http") else f"https://{s}"
        try:
            parsed = urlparse(url)
            domain = (parsed.netloc or parsed.path).split("/")[0].lower()
            domain = re.sub(r"^www\.", "", domain)
            return {"domain": domain, "url": url, "name": None, "city": None}
        except Exception:
            pass

    parts = s.split()
    name = " ".join(parts[:-1]) if len(parts) > 1 else s
    city = parts[-1] if len(parts) > 1 else None
    return {"domain": None, "url": None, "name": name, "city": city}


def safe_get(url: str, timeout: int = 15, headers: dict[str, str] | None = None) -> tuple[int, str]:
    """GET with sane defaults. Returns (status, body) or (0, '') on failure."""
    try:
        import requests
    except ImportError:
        return (0, "")
    h = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/130.0 Safari/537.36 marketing-agency/0.1"
        ),
        "Accept-Language": "en-AU,en;q=0.9",
    }
    if headers:
        h.update(headers)
    try:
        r = requests.get(url, headers=h, timeout=timeout, allow_redirects=True)
        return (r.status_code, r.text[:500_000])
    except Exception:
        return (0, "")


def text_only(html: str, max_chars: int = 20_000) -> str:
    """Extract visible text via BeautifulSoup. Falls back to crude regex if bs4 missing."""
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(" ", strip=True)
    except Exception:
        text = re.sub(r"<[^>]+>", " ", html)
        text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def extract_meta(html: str) -> dict[str, str]:
    """Pull title + description + OG tags + tracking pixel IDs from raw HTML."""
    out: dict[str, str] = {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        if soup.title:
            out["title"] = soup.title.get_text(strip=True)
        for m in soup.find_all("meta"):
            name = (m.get("name") or m.get("property") or "").lower()
            content = m.get("content") or ""
            if name and content:
                out[f"meta:{name}"] = content[:300]
    except Exception:
        m = re.search(r"<title>([^<]{1,200})</title>", html, re.I | re.S)
        if m:
            out["title"] = m.group(1).strip()

    # Tracking pixel signatures
    pixel_patterns = {
        "meta_pixel": r"fbq\(\s*['\"]init['\"]\s*,\s*['\"]?(\d{15,16})['\"]?",
        "ga4": r"G-[A-Z0-9]{8,12}",
        "linkedin_insight": r"_linkedin_partner_id\s*=\s*['\"](\d{4,8})['\"]",
        "google_ads": r"AW-\d{8,12}",
        "tiktok_pixel": r"ttq\.load\(\s*['\"]([A-Z0-9]{18,24})['\"]",
    }
    for key, pat in pixel_patterns.items():
        m = re.search(pat, html)
        if m:
            out[key] = m.group(1) if m.groups() else m.group(0)
    return out
