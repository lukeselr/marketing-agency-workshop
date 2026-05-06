#!/usr/bin/env python3
"""Extract a voice fingerprint from already-scraped sources.

Reads .state/scrape/website.json + linkedin-page.json + instagram-public.json.
Heuristics over the visible copy:
  - average sentence length (tone formality)
  - top vocabulary terms
  - punctuation cadence (em-dashes, exclamation, question)
  - positive vs negative framing (rough)
  - 3 sample sentences pulled verbatim
The user reviews → confirms or asks for re-extraction with different sources.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable

STATE = Path.home() / ".claude/skills/marketing-agency/.state/scrape"
OUT = Path.home() / ".claude/skills/marketing-agency/.state/voice-fingerprint.json"

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "at",
    "for", "with", "by", "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "it", "its", "as", "we", "you", "your",
    "our", "their", "they", "us", "them", "from", "have", "has", "had", "do",
    "does", "did", "will", "would", "can", "could", "should", "may", "might",
    "i", "me", "my", "so", "not", "no", "yes", "all", "any", "more", "most",
    "out", "up", "down", "into", "over", "than", "then", "also", "just",
}


def load(name: str) -> dict:
    p = STATE / f"{name}.json"
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def gather_text(parts: Iterable[str]) -> str:
    return " ".join(p for p in parts if p)


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if 6 <= len(p.split()) <= 40]


def main() -> None:
    web = load("website")
    li = load("linkedin-page")
    ig = load("instagram-public")
    fb = load("facebook-page")

    pieces: list[str] = []
    for p in (web.get("pages") or []):
        pieces.append(p.get("text_excerpt", ""))
    pieces.append(li.get("description", ""))
    pieces.append(ig.get("og_description", ""))
    pieces.append(ig.get("bio") or "")

    text = gather_text(pieces)
    if not text:
        OUT.write_text(json.dumps({
            "status": "no_source_text",
            "note": "Run discover.sh first; no website/social copy found.",
        }, indent=2))
        print(f"Wrote {OUT}")
        return

    sentences = split_sentences(text)
    avg_len = (
        sum(len(s.split()) for s in sentences) / len(sentences)
        if sentences else 0
    )
    words = [w.lower() for w in re.findall(r"[A-Za-z][A-Za-z'-]+", text)]
    content = [w for w in words if w not in STOPWORDS and len(w) > 2]
    top = Counter(content).most_common(20)
    em_dashes = text.count("—") + text.count(" - ")
    exclam = text.count("!")
    questions = text.count("?")

    samples = sentences[:3] if len(sentences) >= 3 else sentences

    fingerprint = {
        "version": 1,
        "sources": {
            "website_pages": len(web.get("pages") or []),
            "linkedin_followers": li.get("followers"),
            "instagram_followers": ig.get("followers"),
            "facebook_likes": fb.get("likes"),
        },
        "metrics": {
            "avg_sentence_words": round(avg_len, 1),
            "em_dash_count": em_dashes,
            "exclamation_count": exclam,
            "question_count": questions,
            "tone": (
                "formal" if avg_len >= 22 else "neutral" if avg_len >= 14 else "casual"
            ),
        },
        "vocabulary_top20": [{"word": w, "count": c} for w, c in top],
        "sample_sentences": samples,
        "rules": [
            "Match the average sentence length within +/- 3 words.",
            "Reuse the top 5 vocabulary terms naturally if they fit the topic.",
            "Mirror em-dash + exclamation cadence; do not exceed measured frequency.",
            "Do not invent statistics or claims absent from the source text.",
        ],
    }

    OUT.write_text(json.dumps(fingerprint, indent=2))
    print(f"Wrote {OUT}")
    print()
    print("== Voice fingerprint summary ==")
    print(f"  Tone: {fingerprint['metrics']['tone']}")
    print(f"  Avg sentence: {fingerprint['metrics']['avg_sentence_words']} words")
    print(f"  Top words: {', '.join(w for w, _ in top[:10])}")
    print()
    print("Sample sentences (verbatim from your sources):")
    for s in samples:
        print(f"  - {s}")
    print()
    print("Confirm in chat: 'sounds like me' / 'try again with X source' / paste a tuning paragraph.")


if __name__ == "__main__":
    main()
