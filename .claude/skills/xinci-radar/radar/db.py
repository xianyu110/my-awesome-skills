from __future__ import annotations

import sqlite3
from pathlib import Path

from radar.paths import DATA, DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS runs (
    run_date TEXT PRIMARY KEY,
    started_at TEXT,
    finished_at TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS run_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    stage TEXT NOT NULL,
    count INTEGER,
    note TEXT
);

CREATE TABLE IF NOT EXISTS domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    source TEXT NOT NULL DEFAULT 'whoisds',
    domain TEXT NOT NULL,
    sld TEXT,
    words TEXT,
    roots TEXT,
    phrase TEXT,
    dns_status TEXT,
    http_status INTEGER,
    classification TEXT,
    title TEXT,
    description TEXT,
    has_pricing INTEGER DEFAULT 0,
    pricing_url TEXT,
    final_url TEXT,
    probed_at TEXT,
    UNIQUE(run_date, source, domain)
);

CREATE TABLE IF NOT EXISTS sitemap_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    site TEXT NOT NULL,
    url TEXT NOT NULL,
    lastmod TEXT,
    slug TEXT,
    slug_phrase TEXT,
    lang_stripped INTEGER DEFAULT 0,
    is_new INTEGER DEFAULT 0,
    UNIQUE(run_date, url)
);

CREATE TABLE IF NOT EXISTS trends_queries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    seed TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    query TEXT NOT NULL,
    relation TEXT NOT NULL,
    value INTEGER,
    formatted_value TEXT,
    layer INTEGER NOT NULL DEFAULT 1,
    UNIQUE(run_date, timeframe, query, seed, relation)
);

CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_date TEXT NOT NULL,
    term TEXT NOT NULL,
    sources TEXT NOT NULL,
    source_count INTEGER NOT NULL,
    pool TEXT,
    mean_5y REAL,
    peak_5y REAL,
    nonzero_weeks INTEGER,
    first_nonzero_week TEXT,
    n_points INTEGER,
    class TEXT,
    yearly_peaks INTEGER,
    recent_max INTEGER,
    evidence TEXT,
    dropped_reason TEXT,
    has_5y INTEGER DEFAULT 0,
    UNIQUE(run_date, term)
);

CREATE TABLE IF NOT EXISTS series_5y (
    term TEXT NOT NULL,
    fetched_at TEXT NOT NULL,
    n_points INTEGER,
    mean REAL,
    peak REAL,
    nonzero_weeks INTEGER,
    first_nonzero_week TEXT,
    yearly_peaks INTEGER,
    recent_max INTEGER,
    class TEXT,
    weekly_json TEXT,
    PRIMARY KEY (term)
);
"""


def connect(path: Path | None = None) -> sqlite3.Connection:
    DATA.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path or DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.executescript(SCHEMA)
    return conn


def log_stat(conn: sqlite3.Connection, run_date: str, stage: str, count: int, note: str = "") -> None:
    conn.execute(
        "INSERT INTO run_stats(run_date, stage, count, note) VALUES (?,?,?,?)",
        (run_date, stage, count, note),
    )
    conn.commit()
