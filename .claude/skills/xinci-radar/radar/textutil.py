from __future__ import annotations

import json
import re
import unicodedata
from functools import lru_cache
from pathlib import Path

import wordninja

from radar.paths import ROOTS_JSON, SYNONYMS_JSON

GENERIC = frozenset(
    {
        "ai",
        "free",
        "online",
        "tool",
        "tools",
        "app",
        "apps",
        "web",
        "website",
        "com",
        "io",
        "net",
        "org",
        "www",
        "best",
        "new",
        "the",
        "and",
        "for",
        "with",
        "from",
        "your",
        "my",
        "a",
        "an",
        "of",
        "to",
        "in",
        "on",
        "by",
    }
)

MODEL_PREFIXES = (
    "veo",
    "wan",
    "krea",
    "sora",
    "kling",
    "runway",
    "gen",
    "gpt",
    "claude",
    "gemini",
    "llama",
    "grok",
    "flux",
    "sdxl",
    "midjourney",
    "pika",
    "luma",
    "hailuo",
    "minimax",
    "ideogram",
    "seedream",
    "wanx",
    "jimeng",
    "keling",
    "vidu",
    "lumaai",
    "openai",
    "anthropic",
    "stable diffusion",
    "stable-diffusion",
    "mj",
)

# Model version numbers like "krea 3", "veo 3.1", "wan 2.7".
_MODEL_RE = re.compile(
    r"\b(?:"
    + "|".join(re.escape(p) for p in MODEL_PREFIXES)
    + r")[\s\-]*v?\d+(?:\.\d+)+\b"
    r"|\b(?:"
    + "|".join(re.escape(p) for p in MODEL_PREFIXES)
    + r")[\s\-]+v?\d+\b",
    re.I,
)

_PUNCT_RE = re.compile(r"[^a-z0-9]+")


@lru_cache(maxsize=1)
def load_roots() -> dict:
    data = json.loads(Path(ROOTS_JSON).read_text(encoding="utf-8"))
    groups = data["groups"]
    flat = []
    for g, items in groups.items():
        for item in items:
            flat.append(item.lower())
    assert len(flat) == 73, f"expected 73 roots, got {len(flat)}"
    return {"groups": groups, "flat": flat, "set": set(flat)}


@lru_cache(maxsize=1)
def load_synonyms() -> list[set[str]]:
    data = json.loads(Path(SYNONYMS_JSON).read_text(encoding="utf-8"))
    return [set(x.lower() for x in group) for group in data["groups"]]


def normalize_chars(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = s.lower().strip()
    s = _PUNCT_RE.sub("", s)
    return s


def tokenize(s: str) -> list[str]:
    s = unicodedata.normalize("NFKC", s or "")
    s = s.lower().replace("_", " ").replace("-", " ")
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    return [t for t in s.split() if t]


def content_words(s: str) -> list[str]:
    return [t for t in tokenize(s) if t not in GENERIC and not t.isdigit()]


def synonym_canonical(token: str) -> str:
    t = token.lower()
    for group in load_synonyms():
        if t in group:
            return sorted(group, key=len)[0]
    return t


def content_words_syn(s: str) -> list[str]:
    return [synonym_canonical(t) for t in content_words(s)]


def jaccard(a: list[str] | set[str], b: list[str] | set[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def is_model_version(term: str) -> bool:
    return bool(_MODEL_RE.search(term or ""))


def segment_sld(sld: str) -> list[str]:
    sld = (sld or "").lower()
    sld = re.sub(r"[^a-z0-9]+", "", sld)
    if not sld:
        return []
    roots = load_roots()["set"]
    # Prefer known roots as whole tokens when they appear as substrings.
    words = wordninja.split(sld)
    # If wordninja smashed a known root, try to recover it.
    joined = "".join(words) if words else sld
    if joined != sld:
        words = wordninja.split(sld)
    return [w for w in words if w]


def phrase_from_words(words: list[str]) -> str:
    return " ".join(w for w in words if w and w not in {"www"})


def extract_matching_roots(sld: str, words: list[str] | None = None) -> list[str]:
    roots = load_roots()["set"]
    s = (sld or "").lower()
    hits = []
    for r in sorted(roots, key=len, reverse=True):
        if len(r) >= 4 and r in s:
            hits.append(r)
        elif r in (words or []):
            hits.append(r)
    # unique preserve order
    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out
