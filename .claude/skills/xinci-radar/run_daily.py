#!/usr/bin/env python3
"""Daily entry: collect three sources, cross-validate, 5y verify, dedup, report."""
from __future__ import annotations

import argparse
import os
import json
import sys
import time
import traceback
from datetime import datetime
from zoneinfo import ZoneInfo

from radar.crossval import build_candidates
from radar.db import connect, log_stat
from radar.dedup import filter_against_published, load_state, writeback
from radar.domains import download_whoisds, filter_interesting, probe_many
from radar.paths import DATA, PUBLISHED_STATE
from radar.report import collect_report_items, write_reports
from radar.sitemaps import harvest, mark_new
from radar.textutil import is_model_version
from radar.trends import TrendsClient, TrendsError, is_useful_related_query, scan_roots
from radar.verify5y import classify_series, fetch_and_classify

TZ = ZoneInfo(os.environ.get("RADAR_TZ", "Asia/Shanghai"))

PROBE_CAP = 320
FILTER_CAP = 800
TRENDS_TIMEFRAMES = ["today 1-m", "now 7-d"]
RECURSE_BREAKOUT_CAP = 15
FIVE_Y_CAP = 40


def today_sg() -> str:
    return datetime.now(TZ).date().isoformat()


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="海外新词雷达日更")
    ap.add_argument("--reuse", action="store_true", help="复用当天库里的原始采集，只补缺失的 5 年序列并重出报告")
    ap.add_argument("--run-date", default="", help="报告日期，默认 RADAR_TZ（Asia/Shanghai）今天")
    ap.add_argument("--reset-published", action="store_true", help="重建报告前清空 published_state.json（首次规则修正时用）")
    return ap.parse_args(argv)


def rec_factory(conn, run_date, stats):
    def rec(stage: str, count: int, note: str = ""):
        stats.append({"stage": stage, "count": count, "note": note})
        log_stat(conn, run_date, stage, count, note)
        print(f"[stat] {stage}: {count} {note}", flush=True)
    return rec


def _jsonish(val, default):
    if val is None:
        return default
    if isinstance(val, (list, dict)):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except json.JSONDecodeError:
            return default
    return default


def load_domain_rows(conn, run_date):
    rows = []
    for r in conn.execute("SELECT * FROM domains WHERE run_date=?", (run_date,)).fetchall():
        row = dict(r)
        row["words"] = _jsonish(row.get("words"), [])
        row["roots"] = _jsonish(row.get("roots"), [])
        rows.append(row)
    return rows


def load_sitemap(conn, run_date):
    rows = [dict(r) for r in conn.execute("SELECT * FROM sitemap_urls WHERE run_date=?", (run_date,)).fetchall()]
    prev = {
        r[0]
        for r in conn.execute(
            "SELECT DISTINCT url FROM sitemap_urls WHERE run_date != ?",
            (run_date,),
        ).fetchall()
    }
    first = len(prev) == 0
    news = [r for r in rows if r.get("is_new")]
    return rows, news, first


def load_trends(conn, run_date):
    kept = []
    raw_n = 0
    for r in conn.execute("SELECT * FROM trends_queries WHERE run_date=?", (run_date,)).fetchall():
        raw_n += 1
        row = dict(r)
        if not is_useful_related_query(row.get("query") or "", row.get("seed") or ""):
            continue
        kept.append(row)
    return kept, raw_n


def attach_5y_from_cache(conn, term):
    cached = conn.execute("SELECT * FROM series_5y WHERE term=?", (term,)).fetchone()
    if not cached:
        return None
    weekly = _jsonish(cached["weekly_json"] if "weekly_json" in cached.keys() else None, None)
    if weekly and len(weekly) >= 200:
        stats_5y = classify_series(weekly)
        if stats_5y.get("ok"):
            return stats_5y
    if cached["n_points"] and cached["n_points"] >= 200:
        return {
            "ok": True,
            "n_points": cached["n_points"],
            "mean": cached["mean"],
            "peak": cached["peak"],
            "nonzero_weeks": cached["nonzero_weeks"],
            "first_nonzero_week": cached["first_nonzero_week"],
            "onset_censored": False,
            "yearly_peaks": cached["yearly_peaks"],
            "recent_max": cached["recent_max"],
            "class": cached["class"],
        }
    return None


def persist_5y(conn, term, got):
    conn.execute(
        """INSERT OR REPLACE INTO series_5y(
            term, fetched_at, n_points, mean, peak, nonzero_weeks,
            first_nonzero_week, yearly_peaks, recent_max, class, weekly_json
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            term,
            datetime.now(TZ).isoformat(timespec="seconds"),
            got["n_points"],
            got["mean"],
            got["peak"],
            got["nonzero_weeks"],
            got["first_nonzero_week"],
            got["yearly_peaks"],
            got["recent_max"],
            got["class"],
            json.dumps(got.get("weekly") or [], ensure_ascii=False),
        ),
    )
    conn.commit()


def persist_candidate(conn, run_date, c):
    conn.execute(
        """INSERT OR REPLACE INTO candidates(
            run_date, term, sources, source_count, pool, mean_5y, peak_5y,
            nonzero_weeks, first_nonzero_week, n_points, class, yearly_peaks,
            recent_max, evidence, dropped_reason, has_5y
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            run_date,
            c["term"],
            json.dumps(c.get("sources") or [], ensure_ascii=False),
            c.get("source_count") or 0,
            c.get("pool"),
            c.get("mean_5y"),
            c.get("peak_5y"),
            c.get("nonzero_weeks"),
            c.get("first_nonzero_week"),
            c.get("n_points"),
            c.get("class"),
            c.get("yearly_peaks"),
            c.get("recent_max"),
            json.dumps(
                {
                    "aliases": c.get("aliases"),
                    "domains": [d.get("domain") for d in c.get("domains") or []],
                    "pages": [p.get("url") for p in c.get("pages") or []],
                    "onset_censored": c.get("onset_censored"),
                },
                ensure_ascii=False,
            ),
            c.get("dropped_reason") or "",
            int(c.get("has_5y") or 0),
        ),
    )
    conn.commit()


def apply_5y(c, stats_5y):
    c = dict(c)
    if stats_5y and stats_5y.get("ok"):
        c["has_5y"] = 1
        c["mean_5y"] = stats_5y["mean"]
        c["peak_5y"] = stats_5y["peak"]
        c["nonzero_weeks"] = stats_5y["nonzero_weeks"]
        c["first_nonzero_week"] = stats_5y["first_nonzero_week"]
        c["onset_censored"] = bool(stats_5y.get("onset_censored"))
        c["n_points"] = stats_5y["n_points"]
        c["class"] = stats_5y["class"]
        c["yearly_peaks"] = stats_5y["yearly_peaks"]
        c["recent_max"] = stats_5y["recent_max"]
    else:
        c["has_5y"] = 0
        c["dropped_reason"] = (c.get("dropped_reason") or "") + " " + (stats_5y or {}).get("reason", "no 5y")
    return c


def main(argv=None) -> int:
    args = parse_args(argv)
    run_date = args.run_date or today_sg()
    reuse = bool(args.reuse)
    started = datetime.now(TZ).isoformat(timespec="seconds")
    conn = connect()
    conn.execute(
        "INSERT OR REPLACE INTO runs(run_date, started_at, notes) VALUES (?,?,?)",
        (run_date, started, "reuse" if reuse else "running"),
    )
    conn.commit()
    stats: list[dict] = []
    source_notes = {"details": {}, "trends_block": ""}
    rec = rec_factory(conn, run_date, stats)

    domain_rows = []
    if reuse:
        domain_rows = load_domain_rows(conn, run_date)
        rec("whoisds_reused", len(domain_rows), f"sqlite rows for {run_date}")
        source_notes["details"]["WhoisDS"] = f"复用库中 {run_date} 的 {len(domain_rows)} 条域名记录，未重新下载日包。"
        counts = {}
        for row in domain_rows:
            k = row.get("classification") or "unknown"
            counts[k] = counts.get(k, 0) + 1
        rec("domains_live", counts.get("live", 0), "")
        rec("domains_unresolved", counts.get("unresolved", 0), "kept as early-bird signal")
        rec("domains_parked", counts.get("parked", 0), "")
        cert_n = sum(1 for r in domain_rows if r.get("source") == "certstream")
        rec("certstream_rows", cert_n, "")
    else:
        try:
            pkg_date, raw_domains, note = download_whoisds(run_date)
            rec("whoisds_raw", len(raw_domains), f"package_date={pkg_date}; {note}")
            source_notes["details"]["WhoisDS"] = f"免费日包 {pkg_date}，原始 {len(raw_domains)} 条。{note}"
            interesting = filter_interesting(raw_domains, cap=FILTER_CAP)
            rec("whoisds_filtered", len(interesting), "junk stripped, tool-root / phrase preferred")
            probe_targets = [x["domain"] for x in interesting]
            print(f"probing {min(len(probe_targets), PROBE_CAP)} domains ...", flush=True)
            t0 = time.time()
            probes = probe_many(probe_targets, cap=PROBE_CAP)
            probe_map = {p["domain"]: p for p in probes}
            rec("whoisds_probed", len(probes), f"{time.time()-t0:.1f}s")
            now = datetime.now(TZ).isoformat(timespec="seconds")
            counts = {"live": 0, "unresolved": 0, "parked": 0, "resolved_no_http": 0, "error": 0}
            for item in interesting:
                p = probe_map.get(item["domain"])
                row = {
                    **item,
                    "run_date": run_date,
                    "source": "whoisds",
                    "dns_status": (p or {}).get("dns_status") or "skipped",
                    "http_status": (p or {}).get("http_status"),
                    "classification": (p or {}).get("classification") or "not_probed",
                    "title": (p or {}).get("title") or "",
                    "description": (p or {}).get("description") or "",
                    "has_pricing": (p or {}).get("has_pricing") or 0,
                    "pricing_url": (p or {}).get("pricing_url") or "",
                    "final_url": (p or {}).get("final_url") or "",
                    "probed_at": now if p else "",
                }
                domain_rows.append(row)
                counts[row["classification"]] = counts.get(row["classification"], 0) + 1
                conn.execute(
                    """INSERT OR REPLACE INTO domains(
                        run_date, source, domain, sld, words, roots, phrase, dns_status,
                        http_status, classification, title, description, has_pricing,
                        pricing_url, final_url, probed_at
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (
                        run_date,
                        "whoisds",
                        row["domain"],
                        row["sld"],
                        json.dumps(row["words"], ensure_ascii=False),
                        json.dumps(row["roots"], ensure_ascii=False),
                        row["phrase"],
                        row["dns_status"],
                        row["http_status"],
                        row["classification"],
                        row["title"],
                        row["description"],
                        int(row["has_pricing"] or 0),
                        row["pricing_url"],
                        row["final_url"],
                        row["probed_at"],
                    ),
                )
            conn.commit()
            rec("domains_live", counts.get("live", 0), "")
            rec("domains_unresolved", counts.get("unresolved", 0), "kept as early-bird signal")
            rec("domains_parked", counts.get("parked", 0), "dropped from priority later")
            source_notes["details"]["域名探针"] = (
                f"候选 {len(interesting)}，实际探针 {len(probes)}。"
                f"live={counts.get('live',0)}, unresolved={counts.get('unresolved',0)}, "
                f"parked={counts.get('parked',0)}, other={sum(v for k,v in counts.items() if k not in ('live','unresolved','parked'))}"
            )
        except Exception as e:
            rec("whoisds_error", 0, f"{type(e).__name__}: {e}")
            source_notes["details"]["WhoisDS"] = f"失败：{type(e).__name__}: {e}"
            traceback.print_exc()

        try:
            cur = conn.execute(
                "SELECT * FROM domains WHERE run_date=? AND source='certstream'",
                (run_date,),
            )
            cert_n = 0
            for r in cur.fetchall():
                cert_n += 1
                row = dict(r)
                row["words"] = _jsonish(row.get("words"), [])
                row["roots"] = _jsonish(row.get("roots"), [])
                domain_rows.append(row)
            rec("certstream_rows", cert_n, "from background listener if running")
        except Exception as e:
            rec("certstream_rows", 0, str(e))

    sitemap_all = []
    sitemap_new = []
    first_sitemap_run = False
    if reuse:
        sitemap_all, sitemap_new, first_sitemap_run = load_sitemap(conn, run_date)
        rec("sitemap_urls", len(sitemap_all), "reused")
        rec("sitemap_new", len(sitemap_new), "first_run" if first_sitemap_run else "diff vs previous runs")
        source_notes["details"]["同行 Sitemap"] = (
            f"复用已收录 {len(sitemap_all)} 条。"
            + (
                "首次运行，没有历史快照，本日不把 URL 标成新增。"
                if first_sitemap_run
                else f"相对历史快照新增 {len(sitemap_new)} 条。"
            )
        )
    else:
        try:
            rows, notes = harvest(run_date)
            prev = {
                r[0]
                for r in conn.execute(
                    "SELECT DISTINCT url FROM sitemap_urls WHERE run_date != ?",
                    (run_date,),
                ).fetchall()
            }
            first_sitemap_run = len(prev) == 0
            rows = mark_new(rows, prev)
            for r in rows:
                conn.execute(
                    """INSERT OR REPLACE INTO sitemap_urls(
                        run_date, site, url, lastmod, slug, slug_phrase, lang_stripped, is_new
                    ) VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        r["run_date"],
                        r["site"],
                        r["url"],
                        r["lastmod"],
                        r["slug"],
                        r["slug_phrase"],
                        r["lang_stripped"],
                        r["is_new"],
                    ),
                )
            conn.commit()
            sitemap_all = rows
            sitemap_new = [r for r in rows if r["is_new"]]
            rec("sitemap_urls", len(rows), json.dumps({k: v["urls"] for k, v in notes.items()}, ensure_ascii=False))
            rec("sitemap_new", len(sitemap_new), "first_run" if first_sitemap_run else "diff vs previous runs")
            source_notes["details"]["同行 Sitemap"] = (
                f"8 个站点共收录 {len(rows)} 条（已剥离语言重复路径）。"
                + (
                    "首次运行，没有历史快照，本日不把 URL 标成新增。"
                    if first_sitemap_run
                    else f"相对历史快照新增 {len(sitemap_new)} 条。"
                )
            )
            source_notes["details"]["Sitemap 分站"] = json.dumps(notes, ensure_ascii=False)
        except Exception as e:
            rec("sitemap_error", 0, f"{type(e).__name__}: {e}")
            source_notes["details"]["同行 Sitemap"] = f"失败：{type(e).__name__}: {e}"
            traceback.print_exc()

    trends_rows = []
    client = TrendsClient(gap=2.6, max_retries=4)
    if reuse:
        trends_rows, raw_n = load_trends(conn, run_date)
        rec("trends_queries_raw_reused", raw_n, "from sqlite")
        rec("trends_queries", len(trends_rows), "after related-query quality filter")
        source_notes["details"]["Google Trends"] = (
            f"复用库中 {raw_n} 条 Rising/Breakout，按「必须带上种子词根、2–6 词、非句子」过滤后剩 {len(trends_rows)} 条。"
        )
    else:
        try:
            prime_note = client.prime()
            rec("trends_prime", 1 if client.primed else 0, prime_note)
            rows, meta = scan_roots(client, TRENDS_TIMEFRAMES, recurse_breakout_cap=RECURSE_BREAKOUT_CAP)
            for r in rows:
                if is_model_version(r["query"]):
                    continue
                trends_rows.append(r)
                conn.execute(
                    """INSERT OR IGNORE INTO trends_queries(
                        run_date, seed, timeframe, query, relation, value, formatted_value, layer
                    ) VALUES (?,?,?,?,?,?,?,?)""",
                    (
                        run_date,
                        r["seed"],
                        r["timeframe"],
                        r["query"],
                        r["relation"],
                        r.get("value"),
                        r.get("formatted_value"),
                        r.get("layer") or 1,
                    ),
                )
            conn.commit()
            rec("trends_queries", len(trends_rows), json.dumps({k: meta["timeframes"].get(k) for k in meta.get("timeframes", {})}, ensure_ascii=False))
            source_notes["details"]["Google Trends"] = (
                f"词根 73 个，时间窗 {TRENDS_TIMEFRAMES}，有效 Rising/Breakout {len(trends_rows)} 条；"
                f"接口调用 {meta.get('calls')} 次。"
                + ((" 被限流：" + meta.get("block_note", "")) if meta.get("blocked") else "")
            )
            if meta.get("blocked"):
                source_notes["trends_block"] = meta.get("block_note") or "Trends blocked"
            if meta.get("errors"):
                source_notes["details"]["Trends 错误"] = " | ".join(meta["errors"][:8])
        except Exception as e:
            rec("trends_error", 0, f"{type(e).__name__}: {e}")
            source_notes["details"]["Google Trends"] = f"失败：{type(e).__name__}: {e}"
            if getattr(client, "block_note", ""):
                source_notes["trends_block"] = client.block_note
            traceback.print_exc()

    cands = build_candidates(domain_rows, sitemap_new, trends_rows)
    rec("candidates_raw", len(cands), "")
    rec("candidates_priority", sum(1 for c in cands if c["pool"] == "priority"), "2+ sources")
    rec("candidates_watch", sum(1 for c in cands if c["pool"] == "watch"), "single source")
    rec("candidates_dropped_pre_dedup", sum(1 for c in cands if c["pool"] == "dropped"), "")

    if args.reset_published:
        PUBLISHED_STATE.write_text(
            json.dumps({"terms": [], "domains": [], "history": []}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        rec("published_state_reset", 0, "cleared before rebuild")

    state = load_state()
    cands = filter_against_published(cands, state)
    rec("candidates_dropped_dedup", sum(1 for c in cands if str(c.get("dropped_reason") or "").startswith("dedup")), "five-layer published-state")

    def priority_key(c):
        breakout = any(t.get("relation") == "breakout" for t in c.get("trends") or [])
        pricing = any(d.get("has_pricing") for d in c.get("domains") or [])
        toolish = 0 if any((d.get("roots") or []) for d in c.get("domains") or []) or any(
            t.get("seed") for t in c.get("trends") or []
        ) else 1
        return (
            0 if c["pool"] == "priority" else 1,
            0 if breakout else 1,
            0 if pricing else 1,
            toolish,
            -c["source_count"],
            c["term"],
        )

    need_5y = [c for c in cands if c["pool"] in {"priority", "watch"} and not is_model_version(c["term"])]
    need_5y.sort(key=priority_key)
    selected = need_5y[:FIVE_Y_CAP]
    rec("five_y_selected", len(selected), f"cap={FIVE_Y_CAP}, never batched with other keywords")

    classified = []
    ok_n = 0
    for i, c in enumerate(selected, 1):
        term = c["term"]
        stats_5y = attach_5y_from_cache(conn, term)
        if stats_5y:
            print(f"  5y cache {i}/{len(selected)} {term}", flush=True)
        else:
            try:
                if reuse and not client.primed:
                    print(client.prime(), flush=True)
                print(f"  5y fetch {i}/{len(selected)} {term}", flush=True)
                got = fetch_and_classify(client, term)
                persist_5y(conn, term, got)
                stats_5y = got
            except TrendsError as e:
                print(f"  5y fail {term}: {e}", flush=True)
                c = dict(c)
                c["has_5y"] = 0
                c["dropped_reason"] = (c.get("dropped_reason") or "") + f" 5y_fail: {e}"
                classified.append(c)
                persist_candidate(conn, run_date, c)
                if client.blocked:
                    source_notes["trends_block"] = client.block_note or str(e)
                    for rest in selected[i:]:
                        rest = dict(rest)
                        rest["has_5y"] = 0
                        rest["dropped_reason"] = (rest.get("dropped_reason") or "") + " 5y_skipped_blocked"
                        classified.append(rest)
                    break
                continue
        c = apply_5y(c, stats_5y)
        if c.get("has_5y"):
            ok_n += 1
        classified.append(c)
        persist_candidate(conn, run_date, c)

    rec("five_y_ok", ok_n, "terms with usable ~262-week series; others cannot enter keyword sections")

    done_terms = {c["term"] for c in classified}
    for c in cands:
        if c["term"] not in done_terms:
            cc = dict(c)
            cc["has_5y"] = 0
            classified.append(cc)

    sections = collect_report_items(classified, domain_rows, sitemap_new, first_sitemap_run)
    rec("report_pure_new", len(sections["纯新词"]), "")
    rec("report_seasonal", len(sections["周期回潮"]), "")
    rec("report_evergreen", len(sections["老词翻红仅标注"]), "annotated only, never called first breakout")
    rec("report_early_domains", len(sections["新域名早鸟"]), "")
    rec("report_new_pages", len(sections["同行新页面"]), "0 on first sitemap run")

    md_path, html_path = write_reports(run_date, sections, stats, source_notes)

    report_terms = [c["term"] for sec in ("纯新词", "周期回潮", "老词翻红仅标注") for c in sections[sec]]
    report_domains = [d.get("domain") for d in sections["新域名早鸟"] if d.get("domain")]
    writeback(state, report_terms, report_domains, run_date)
    rec("published_state_terms", len(load_state().get("terms") or []), str(DATA / "published_state.json"))

    finished = datetime.now(TZ).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE runs SET finished_at=?, notes=? WHERE run_date=?",
        (finished, json.dumps({"md": str(md_path), "html": str(html_path), "reuse": reuse}, ensure_ascii=False), run_date),
    )
    conn.commit()
    print(f"\nReport written:\n  {md_path}\n  {html_path}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
