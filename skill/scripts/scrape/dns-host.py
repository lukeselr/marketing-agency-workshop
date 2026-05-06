#!/usr/bin/env python3
"""Detect site host via DNS + optional whois. Outputs only the hints we use.

Whois output is HEAVILY trimmed (origin country only) — never piped raw to
synthesize.py.
"""
from __future__ import annotations

import re
import subprocess
import sys

from _helpers import emit, normalise_input


def dig(domain: str, record: str = "A") -> list[str]:
    try:
        out = subprocess.check_output(
            ["dig", "+short", "+time=3", "+tries=2", record, domain],
            text=True, timeout=8,
        )
        return [line.strip() for line in out.splitlines() if line.strip()]
    except Exception:
        return []


def whois_country(domain: str) -> str | None:
    """Pull country code from whois with a hard 8-second timeout."""
    try:
        out = subprocess.check_output(
            ["whois", domain], text=True, timeout=8,
        )
    except Exception:
        return None
    for line in out.splitlines():
        m = re.match(r"\s*country:\s*(\S+)", line, re.I)
        if m:
            return m.group(1).strip()
    return None


def main() -> None:
    raw = sys.argv[1] if len(sys.argv) > 1 else ""
    inp = normalise_input(raw)
    if not inp["domain"]:
        emit({"scraper": "dns-host", "status": "skipped", "reason": "no domain"})
        return

    domain = inp["domain"]
    a = dig(domain, "A")
    aaaa = dig(domain, "AAAA")
    cname = dig(domain, "CNAME")
    mx = dig(domain, "MX")
    ns = dig(domain, "NS")

    # Cross-reference all DNS data for host signature
    haystack = " ".join(cname + a + aaaa + ns).lower()
    mx_low = " ".join(mx).lower()
    hints: list[str] = []
    rules = [
        ("framer", "framer"),
        ("vercel", "vercel"),
        ("netlify", "netlify"),
        ("shopify", "shopify"),
        ("squarespace", "squarespace"),
        ("wix", "wixdns"),
        ("wix", "wix.com"),
        ("cloudflare-cdn", "cloudflare"),
        ("ghl", "leadconnectorhq"),
        ("ghl", "msgsndr"),
    ]
    seen: set[str] = set()
    for label, needle in rules:
        if needle in haystack and label not in seen:
            hints.append(label)
            seen.add(label)
    # Email host
    if "google" in mx_low or "googlemail" in mx_low:
        hints.append("google-workspace-email")
    if "outlook" in mx_low or "office365" in mx_low or "protection.outlook" in mx_low:
        hints.append("microsoft-365-email")
    # Squarespace via NS
    if any("squarespacedns" in n.lower() for n in ns):
        if "squarespace" not in seen:
            hints.append("squarespace")

    country = whois_country(domain)

    emit({
        "scraper": "dns-host",
        "status": "ok",
        "input": inp,
        "domain": domain,
        "a": a,
        "aaaa": aaaa,
        "cname": cname,
        "mx": mx,
        "ns": ns,
        "host_hints": hints,
        "registrar_country": country,
    })


if __name__ == "__main__":
    main()
