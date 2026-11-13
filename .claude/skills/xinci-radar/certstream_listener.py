#!/usr/bin/env python3
"""
Optional Certificate Transparency listener.

New hostnames appear in public CT logs when they first request a TLS certificate.
This process writes matching domains into the same SQLite database used by
run_daily.py (source='certstream'). It does not replace the WhoisDS daily pack:
WhoisDS still covers domains that were registered but have not yet requested a cert.

Usage:
  .venv/bin/python certstream_listener.py

The box must be able to reach wss://certstream.calidog.io. If the websocket
cannot connect, leave this process off; the daily job still runs on WhoisDS.
"""
from __future__ import annotations

import json
import re
import signal
import sys
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from radar.db import connect
from radar.domains import is_junk_domain, split_domain
from radar.paths import DATA
from radar.textutil import extract_matching_roots, phrase_from_words, segment_sld

TZ = ZoneInfo("Asia/Singapore")
URL = "wss://certstream.calidog.io/"
STOP = False


def _stop(*_):
    global STOP
    STOP = True


def interesting(host: str) -> dict | None:
    host = host.lower().strip().lstrip("*.")
    if not host or " " in host:
        return None
    if is_junk_domain(host):
        return None
    sld, tld = split_domain(host)
    words = segment_sld(sld)
    roots = extract_matching_roots(sld, words)
    if not roots and len([w for w in words if len(w) >= 4]) < 2:
        return None
    return {
        "domain": host,
        "sld": sld,
        "words": words,
        "roots": roots,
        "phrase": phrase_from_words(words),
    }


def main() -> int:
    try:
        import certstream
    except ImportError:
        print("certstream package is not installed. pip install certstream", file=sys.stderr)
        return 2

    DATA.mkdir(parents=True, exist_ok=True)
    conn = connect()
    seen = set()
    stats = {"msg": 0, "kept": 0, "skip": 0}

    def callback(message, context):
        if STOP:
            raise KeyboardInterrupt
        if not message or message.get("message_type") != "certificate_update":
            return
        stats["msg"] += 1
        data = message.get("data") or {}
        leaf = data.get("leaf_cert") or {}
        names = list(leaf.get("all_domains") or [])
        run_date = datetime.now(TZ).date().isoformat()
        now = datetime.now(TZ).isoformat(timespec="seconds")
        for name in names:
            info = interesting(name)
            if not info:
                stats["skip"] += 1
                continue
            key = (run_date, info["domain"])
            if key in seen:
                continue
            seen.add(key)
            conn.execute(
                """INSERT OR IGNORE INTO domains(
                    run_date, source, domain, sld, words, roots, phrase, dns_status,
                    http_status, classification, title, description, has_pricing,
                    pricing_url, final_url, probed_at
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    run_date,
                    "certstream",
                    info["domain"],
                    info["sld"],
                    json.dumps(info["words"], ensure_ascii=False),
                    json.dumps(info["roots"], ensure_ascii=False),
                    info["phrase"],
                    "unknown",
                    None,
                    "cert_seen",
                    "",
                    "",
                    0,
                    "",
                    "",
                    now,
                ),
            )
            stats["kept"] += 1
            if stats["kept"] % 20 == 0:
                conn.commit()
                print(f"[{now}] certstream kept={stats['kept']} msgs={stats['msg']} last={info['domain']}", flush=True)

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)
    print(f"Connecting to {URL} ...", flush=True)
    try:
        certstream.listen_for_events(callback, url=URL)
    except KeyboardInterrupt:
        print("stopped", flush=True)
    except Exception as e:
        print(f"certstream failed: {type(e).__name__}: {e}", file=sys.stderr)
        return 1
    finally:
        conn.commit()
        print(json.dumps(stats), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
