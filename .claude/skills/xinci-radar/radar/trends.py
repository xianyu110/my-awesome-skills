from __future__ import annotations

import json
import time
from typing import Any

import requests

from radar.domains import USER_AGENT
from radar.textutil import load_roots, tokenize, GENERIC, is_model_version

EXPLORE = "https://trends.google.com/trends/api/explore"
RELATED = "https://trends.google.com/trends/api/widgetdata/relatedsearches"
MULTILINE = "https://trends.google.com/trends/api/widgetdata/multiline"
HOME = "https://trends.google.com/"


class TrendsError(Exception):
    def __init__(self, message: str, status: int | None = None, body: str = ""):
        super().__init__(message)
        self.status = status
        self.body = body


def strip_xssi(text: str) -> Any:
    idx = text.find("{")
    if idx < 0:
        raise TrendsError("no JSON object in Trends response", body=text[:300])
    return json.loads(text[idx:])


class TrendsClient:
    def __init__(self, gap: float = 2.5, max_retries: int = 4):
        self.sess = requests.Session()
        self.sess.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://trends.google.com/trends/explore",
            }
        )
        self.gap = gap
        self.max_retries = max_retries
        self._last = 0.0
        self.primed = False
        self.blocked = False
        self.block_note = ""
        self.calls = 0
        self.errors: list[str] = []

    def _sleep_gap(self):
        now = time.time()
        wait = self.gap - (now - self._last)
        if wait > 0:
            time.sleep(wait)

    def prime(self) -> str:
        try:
            r = self.sess.get(HOME, timeout=20)
            self.primed = r.status_code == 200 or "NID" in self.sess.cookies.get_dict()
            note = f"GET {HOME} -> {r.status_code}, cookies={list(self.sess.cookies.get_dict())}"
            if r.status_code == 429:
                self.block_note = note + " (homepage 429, may still work)"
            return note
        except requests.RequestException as e:
            self.blocked = True
            self.block_note = f"prime failed: {type(e).__name__}: {e}"
            return self.block_note

    def _get(self, url: str, params: dict) -> Any:
        if self.blocked and "hard" in self.block_note:
            raise TrendsError(self.block_note)
        backoff = 20.0
        last_err = None
        for attempt in range(self.max_retries):
            self._sleep_gap()
            try:
                r = self.sess.get(url, params=params, timeout=25)
                self._last = time.time()
                self.calls += 1
                if r.status_code == 429:
                    last_err = TrendsError("HTTP 429", status=429, body=r.text[:300])
                    self.errors.append(f"429 on {url} attempt {attempt+1}")
                    time.sleep(backoff)
                    backoff = min(backoff * 2, 120)
                    # re-prime
                    self.prime()
                    continue
                if r.status_code != 200:
                    last_err = TrendsError(f"HTTP {r.status_code}", status=r.status_code, body=r.text[:300])
                    self.errors.append(f"{r.status_code} on {url}")
                    if r.status_code in {403, 401}:
                        time.sleep(backoff)
                        backoff = min(backoff * 2, 120)
                        continue
                    raise last_err
                return strip_xssi(r.text)
            except TrendsError:
                raise
            except Exception as e:
                last_err = TrendsError(f"{type(e).__name__}: {e}")
                self.errors.append(str(last_err))
                time.sleep(backoff)
                backoff = min(backoff * 2, 120)
        # exhausted
        if last_err and getattr(last_err, "status", None) == 429:
            self.blocked = True
            self.block_note = f"Google Trends blocked/rate-limited this box IP after {self.calls} calls: {last_err.body}"
        raise last_err or TrendsError("Trends request failed")

    def explore(self, keywords: list[str], timeframe: str) -> dict:
        req = {
            "comparisonItem": [{"keyword": k, "geo": "", "time": timeframe} for k in keywords],
            "category": 0,
            "property": "",
        }
        return self._get(EXPLORE, {"hl": "en-US", "tz": "0", "req": json.dumps(req, separators=(",", ":"))})

    def related_rising(self, keywords: list[str], timeframe: str) -> list[dict]:
        data = self.explore(keywords, timeframe)
        widgets = data.get("widgets") or []
        rows = []
        for w in widgets:
            wid = str(w.get("id") or "")
            if not wid.startswith("RELATED_QUERIES"):
                continue
            seed = w.get("keywordName") or ""
            token = w.get("token")
            wreq = w.get("request")
            if not token or not wreq:
                continue
            payload = self._get(
                RELATED,
                {
                    "hl": "en-US",
                    "tz": "0",
                    "req": json.dumps(wreq, separators=(",", ":")),
                    "token": token,
                },
            )
            ranked = (payload.get("default") or {}).get("rankedList") or []
            # list 0 = TOP, list 1 = RISING
            if len(ranked) < 2:
                continue
            rising = ranked[1].get("rankedKeyword") or []
            for it in rising:
                q = (it.get("query") or "").strip()
                if not q:
                    continue
                formatted = str(it.get("formattedValue") or "")
                raw = it.get("value")
                try:
                    value = int(raw)
                except (TypeError, ValueError):
                    value = 0
                is_breakout = formatted.lower() == "breakout" or value >= 5000
                if not is_useful_related_query(q, seed):
                    continue
                rows.append(
                    {
                        "seed": seed,
                        "timeframe": timeframe,
                        "query": q,
                        "relation": "breakout" if is_breakout else "rising",
                        "value": value,
                        "formatted_value": formatted,
                    }
                )
        return rows

    def series_5y(self, term: str) -> dict:
        """Fetch today 5-y series for a SINGLE term. Never batch with other words."""
        data = self.explore([term], "today 5-y")
        widgets = data.get("widgets") or []
        ts = next((w for w in widgets if str(w.get("id") or "") == "TIMESERIES"), None)
        if not ts or not ts.get("token") or not ts.get("request"):
            raise TrendsError(f"no TIMESERIES widget for {term!r}")
        payload = self._get(
            MULTILINE,
            {
                "hl": "en-US",
                "tz": "0",
                "req": json.dumps(ts["request"], separators=(",", ":")),
                "token": ts["token"],
            },
        )
        points = (payload.get("default") or {}).get("timelineData") or []
        weekly = []
        for p in points:
            vals = p.get("value") or [0]
            try:
                v = int(vals[0])
            except (TypeError, ValueError):
                v = 0
            # hasData false should not be treated as a real 0-interest week if missing
            has = p.get("hasData")
            has_data = True if has is None else bool(has[0] if isinstance(has, list) else has)
            weekly.append(
                {
                    "time": p.get("time"),
                    "week_label": p.get("formattedAxisTime") or p.get("formattedTime"),
                    "value": v if has_data else None,
                    "has_data": has_data,
                    "is_partial": bool(p.get("isPartial")),
                }
            )
        return {"term": term, "points": weekly}



def is_useful_related_query(query: str, seed: str) -> bool:
    """Keep tool-like related queries; drop news headlines and loose one-word jumps."""
    q = (query or "").strip()
    if not q or is_model_version(q):
        return False
    if len(q) < 4 or len(q) > 70:
        return False
    if any(ch in q for ch in ".?!:;。？"):
        return False
    tokens = tokenize(q)
    if len(tokens) < 2 or len(tokens) > 6:
        return False
    seed_toks = tokenize(seed) or [seed.lower()]
    qset = set(tokens)
    if not any(s in qset or s in q.lower().replace(" ", "") for s in seed_toks if len(s) >= 4 or s == "pfp"):
        # allow synonym roots (converter/convert etc. handled by token inclusion)
        from radar.textutil import synonym_canonical
        syn_seed = {synonym_canonical(s) for s in seed_toks}
        syn_q = {synonym_canonical(t) for t in tokens}
        if not (syn_seed & syn_q):
            return False
    return True


def batched(items: list, n: int) -> list[list]:
    return [items[i : i + n] for i in range(0, len(items), n)]


def scan_roots(client: TrendsClient, timeframes: list[str], recurse_breakout_cap: int = 20) -> tuple[list[dict], dict]:
    roots = load_roots()["flat"]
    assert len(roots) == 73
    all_rows: list[dict] = []
    meta = {"timeframes": {}, "recursion": {}, "errors": []}
    for tf in timeframes:
        tf_rows = []
        for batch in batched(roots, 5):
            try:
                rows = client.related_rising(batch, tf)
                for r in rows:
                    r["layer"] = 1
                tf_rows.extend(rows)
            except TrendsError as e:
                note = f"{tf} batch {batch}: {e}"
                meta["errors"].append(note)
                if client.blocked:
                    meta["timeframes"][tf] = {"layer1": len(tf_rows), "blocked": True, "error": note}
                    break
        meta["timeframes"].setdefault(tf, {})["layer1"] = len(tf_rows)
        # second-level recursion on Breakout terms
        if not client.blocked:
            seeds = []
            seen = set()
            for r in tf_rows:
                if r["relation"] == "breakout":
                    q = r["query"].strip().lower()
                    if q and q not in seen and q not in {x.lower() for x in roots}:
                        seen.add(q)
                        seeds.append(r["query"].strip())
            seeds = seeds[:recurse_breakout_cap]
            rec_rows = []
            for batch in batched(seeds, 5):
                try:
                    rows = client.related_rising(batch, tf)
                    for r in rows:
                        r["layer"] = 2
                    rec_rows.extend(rows)
                except TrendsError as e:
                    meta["errors"].append(f"recursion {tf} {batch}: {e}")
                    if client.blocked:
                        break
            meta["timeframes"][tf]["layer2_seeds"] = seeds
            meta["timeframes"][tf]["layer2"] = len(rec_rows)
            tf_rows.extend(rec_rows)
        all_rows.extend(tf_rows)
        if client.blocked:
            break
    meta["blocked"] = client.blocked
    meta["block_note"] = client.block_note
    meta["calls"] = client.calls
    meta["client_errors"] = client.errors
    return all_rows, meta
