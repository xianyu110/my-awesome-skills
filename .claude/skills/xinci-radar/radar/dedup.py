from __future__ import annotations

import json
from pathlib import Path

from radar.paths import PUBLISHED_STATE
from radar.textutil import content_words, content_words_syn, jaccard, normalize_chars


def load_state(path: Path | None = None) -> dict:
    p = path or PUBLISHED_STATE
    if not p.exists():
        return {"terms": [], "domains": [], "history": []}
    return json.loads(p.read_text(encoding="utf-8"))


def save_state(state: dict, path: Path | None = None) -> None:
    p = path or PUBLISHED_STATE
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def layer1_norm_hit(term: str, published_terms: list[str]) -> str | None:
    nt = normalize_chars(term)
    if not nt:
        return "empty"
    for prev in published_terms:
        if normalize_chars(prev) == nt:
            return f"normalized equal to published {prev!r}"
    return None


def layer2_jaccard_hit(term: str, published_terms: list[str]) -> str | None:
    cur = content_words(term)
    if len(cur) < 2:
        return None
    for prev in published_terms:
        prev_w = content_words(prev)
        inter = set(cur) & set(prev_w)
        if len(inter) >= 2 and jaccard(cur, prev_w) >= 0.5:
            return f"jaccard with {prev!r} inter={sorted(inter)}"
    return None


def layer3_synonym_hit(term: str, published_terms: list[str]) -> str | None:
    cur = content_words_syn(term)
    if len(cur) < 2:
        return None
    for prev in published_terms:
        prev_w = content_words_syn(prev)
        inter = set(cur) & set(prev_w)
        if len(inter) >= 2 and jaccard(cur, prev_w) >= 0.5:
            return f"synonym-jaccard with {prev!r} inter={sorted(inter)}"
    return None


def layer4_domain_root_hit(term: str, domains: list[str], published_terms: list[str], published_domains: list[str]) -> str | None:
    nt = normalize_chars(term)
    for prev in published_terms:
        np = normalize_chars(prev)
        if not np or not nt:
            continue
        if len(np) >= 5 and np in nt:
            return f"new term contains published root {prev!r}"
        if len(nt) >= 5 and nt in np:
            return f"published term {prev!r} contains new term"
    for d in domains:
        nd = normalize_chars(d)
        for prev in published_terms:
            np = normalize_chars(prev)
            if len(np) >= 5 and np in nd:
                return f"new domain {d!r} contains published term {prev!r}"
        for pd in published_domains:
            # if same domain already published
            if normalize_chars(pd) == nd:
                return f"domain {d!r} already published"
    for pd in published_domains:
        npd = normalize_chars(pd)
        if len(nt) >= 5 and nt in npd:
            return f"new term appears inside published domain {pd!r}"
    return None


def filter_against_published(candidates: list[dict], state: dict) -> list[dict]:
    published_terms = list(state.get("terms") or [])
    published_domains = list(state.get("domains") or [])
    out = []
    for c in candidates:
        if c.get("pool") == "dropped":
            out.append(c)
            continue
        domains = [d.get("domain") for d in c.get("domains") or [] if d.get("domain")]
        reasons = []
        r1 = layer1_norm_hit(c["term"], published_terms)
        if r1:
            reasons.append("L1:" + r1)
        r2 = layer2_jaccard_hit(c["term"], published_terms)
        if r2:
            reasons.append("L2:" + r2)
        r3 = layer3_synonym_hit(c["term"], published_terms)
        if r3:
            reasons.append("L3:" + r3)
        r4 = layer4_domain_root_hit(c["term"], domains, published_terms, published_domains)
        if r4:
            reasons.append("L4:" + r4)
        if reasons:
            c = dict(c)
            c["pool"] = "dropped"
            c["dropped_reason"] = "dedup: " + " | ".join(reasons)
        out.append(c)
    return out


def writeback(state: dict, report_terms: list[str], report_domains: list[str], run_date: str) -> dict:
    terms = list(state.get("terms") or [])
    domains = list(state.get("domains") or [])
    seen_t = {normalize_chars(t) for t in terms}
    seen_d = {normalize_chars(d) for d in domains}
    added_t, added_d = [], []
    for t in report_terms:
        n = normalize_chars(t)
        if n and n not in seen_t:
            terms.append(t)
            seen_t.add(n)
            added_t.append(t)
    for d in report_domains:
        n = normalize_chars(d)
        if n and n not in seen_d:
            domains.append(d)
            seen_d.add(n)
            added_d.append(d)
    history = list(state.get("history") or [])
    history.append({"run_date": run_date, "added_terms": added_t, "added_domains": added_d})
    new_state = {"terms": terms, "domains": domains, "history": history}
    save_state(new_state)
    return new_state
