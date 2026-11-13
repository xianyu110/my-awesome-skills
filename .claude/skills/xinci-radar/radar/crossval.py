from __future__ import annotations

import re
from collections import defaultdict

from radar.textutil import (
    content_words,
    content_words_syn,
    is_model_version,
    jaccard,
    load_roots,
    normalize_chars,
    tokenize,
)


def _tokens(s: str) -> list[str]:
    return content_words(s)


# Common leftover words that should not glue two different topics together.
WEAK = frozenset({
    "list", "lists", "code", "codes", "studio", "program", "day", "national",
    "space", "player", "official", "home", "free", "best", "new", "zero",
    "pro", "app", "apps", "official", "legal", "challenge", "update", "updates",
    "near", "me", "jobs", "job", "salary", "price", "cost", "review", "reviews",
})


# Verb / product-suffix roots should not glue two topics; topical roots (meme, avatar…) may.
SUFFIX_ROOTS = frozenset({
    "translator", "processor", "designer", "compiler", "analyzer", "evaluator",
    "sender", "receiver", "interpreter", "uploader", "calculator", "generator",
    "builder", "checker", "detector", "scraper", "manager", "explorer",
    "dashboard", "planner", "tracker", "recorder", "optimizer", "scheduler",
    "converter", "viewer", "extractor", "convert", "monitor", "notifier",
    "verifier", "simulator", "assistant", "constructor", "comparator",
    "navigator", "syncer", "connector", "online", "cataloger", "responder",
    "downloader", "maker", "creator", "editor", "guide", "compressor",
    "upscaler", "enhancer", "remover", "resizer", "cropper", "subtitler",
    "merger", "splitter", "transcriber", "vectorizer", "colorizer",
    "format", "sample", "scheme", "example",
})


def _distinctive(tokens: list[str]) -> set[str]:
    return {t for t in tokens if t not in SUFFIX_ROOTS and t not in WEAK and len(t) >= 3}


def terms_match(a: str, b: str) -> bool:
    if not a or not b:
        return False
    na, nb = normalize_chars(a), normalize_chars(b)
    if not na or not nb:
        return False
    if na == nb:
        return True
    ta, tb = _tokens(a), _tokens(b)
    # A single leftover token may only exact-match, never as a substring of a longer phrase.
    if len(ta) < 2 or len(tb) < 2:
        return False
    # Whole-phrase concatenation, e.g. "meme generator" vs domain "memegenerator".
    if len(na) >= 8 and len(nb) >= 8 and (na in nb or nb in na):
        # still require a shared distinctive token to avoid "listmaker" vs "christmaslistmaker"
        if _distinctive(ta) & _distinctive(tb) or _distinctive(content_words_syn(a)) & _distinctive(content_words_syn(b)):
            return True
    sa, sb = set(ta), set(tb)
    dist = _distinctive(ta) & _distinctive(tb)
    if dist and len(sa) >= 2 and len(sb) >= 2 and (sa <= sb or sb <= sa):
        return True
    if dist and len(sa & sb) >= 2 and jaccard(sa, sb) >= 0.5:
        return True
    syn_a, syn_b = set(content_words_syn(a)), set(content_words_syn(b))
    dist_syn = _distinctive(list(syn_a)) & _distinctive(list(syn_b))
    if dist_syn and len(syn_a) >= 2 and len(syn_b) >= 2 and (syn_a <= syn_b or syn_b <= syn_a):
        return True
    if dist_syn and len(syn_a & syn_b) >= 2 and jaccard(syn_a, syn_b) >= 0.5:
        return True
    return False


def is_brand_noise(term: str, src_types: set[str], parked: bool) -> str | None:
    if parked and src_types <= {"domain"}:
        return "parked"
    if is_model_version(term):
        return "model_version"
    words = _tokens(term)
    # single generic leftover
    if not words:
        return "empty_after_generic_strip"
    if len(words) == 1 and words[0] in {"online", "ai", "app", "tool"}:
        return "generic"
    return None


def build_candidates(
    domain_rows: list[dict],
    sitemap_new: list[dict],
    trends_rows: list[dict],
) -> list[dict]:
    """
    domain_rows: phrase, domain, classification, roots, title (title never used as main term)
    sitemap_new: slug_phrase, url, site, lastmod
    trends_rows: query, relation, seed, layer, timeframe
    """
    # Collect items per source with a display term.
    # Core term for domains MUST come from domain word roots / segmented SLD, never page title.
    items = []
    for d in domain_rows:
        phrase = (d.get("phrase") or "").strip()
        if not phrase:
            continue
        items.append(
            {
                "term": phrase,
                "source": "domain",
                "payload": d,
            }
        )
    for s in sitemap_new:
        phrase = (s.get("slug_phrase") or "").strip()
        if not phrase or len(phrase) < 3:
            continue
        items.append({"term": phrase, "source": "sitemap", "payload": s})
    for t in trends_rows:
        q = (t.get("query") or "").strip()
        if not q:
            continue
        items.append({"term": q, "source": "trends", "payload": t})

    # Cluster matching terms. Prefer a Trends query as the canonical name when present
    # (usually a full search phrase); otherwise the longest phrase.
    clusters: list[dict] = []
    for item in items:
        placed = False
        for c in clusters:
            if terms_match(item["term"], c["term"]) or any(terms_match(item["term"], t) for t in c["terms"]):
                c["items"].append(item)
                c["terms"].append(item["term"])
                c["sources"].add(item["source"])
                placed = True
                break
        if not placed:
            clusters.append(
                {
                    "term": item["term"],
                    "terms": [item["term"]],
                    "sources": {item["source"]},
                    "items": [item],
                }
            )

    cands = []
    for c in clusters:
        # canonical term
        trends_terms = [i["term"] for i in c["items"] if i["source"] == "trends"]
        if trends_terms:
            term = max(trends_terms, key=lambda s: (len(s), s))
        else:
            term = max(c["terms"], key=lambda s: (len(tokenize(s)), len(s)))

        src_types = set(c["sources"])
        domains = [i["payload"] for i in c["items"] if i["source"] == "domain"]
        pages = [i["payload"] for i in c["items"] if i["source"] == "sitemap"]
        trends = [i["payload"] for i in c["items"] if i["source"] == "trends"]
        parked = bool(domains) and all(d.get("classification") == "parked" for d in domains)
        reason = is_brand_noise(term, src_types, parked)
        # If mixed parked + other sources, don't drop the cluster; just note parking.
        if reason == "parked" and src_types - {"domain"}:
            reason = None
        source_count = len(src_types)
        if reason:
            pool = "dropped"
        elif source_count >= 2:
            pool = "priority"
        else:
            pool = "watch"
        cands.append(
            {
                "term": term,
                "aliases": sorted(set(c["terms"])),
                "sources": sorted(src_types),
                "source_count": source_count,
                "pool": pool,
                "dropped_reason": reason or "",
                "domains": domains,
                "pages": pages,
                "trends": trends,
            }
        )
    cands.sort(key=lambda x: (-x["source_count"], x["term"]))
    return cands
