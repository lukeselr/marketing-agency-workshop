#!/usr/bin/env python3
"""Site host detector with confidence score. Reads dns-host scrape + website tracking pixels."""
from __future__ import annotations
import json, sys
from pathlib import Path

STATE = Path.home() / ".claude/skills/marketing-agency/.state/scrape"

def detect():
    dns = json.loads((STATE / "dns-host.json").read_text()) if (STATE / "dns-host.json").is_file() else {}
    web = json.loads((STATE / "website.json").read_text()) if (STATE / "website.json").is_file() else {}
    hints = dns.get("host_hints") or []
    pixels = (web.get("tracking_pixels_detected") or {})
    confidence = 0
    host = "unknown"
    if hints:
        host = hints[0]
        confidence = 70
    if "framer" in hints and "vercel" in hints:
        host = "framer"
        confidence = 90
    if pixels.get("ga4") and "shopify" in hints:
        host = "shopify"
        confidence = 95
    return {"host": host, "confidence": confidence, "all_hints": hints, "pixels": list(pixels.keys())}

if __name__ == "__main__":
    print(json.dumps(detect(), indent=2))
