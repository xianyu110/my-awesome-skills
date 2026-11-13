from __future__ import annotations

import html
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from radar.paths import REPORTS

TZ = ZoneInfo("Asia/Singapore")

SECTION_DEFS = [
    ("纯新词", "纯血从零突发", "过去 5 年底盘均值低、近期突然拉升。首次起量周一律取自 Trends 262 周序列，不用页面 lastmod。"),
    ("周期回潮", "年度周期回潮", "5 年曲线在相近季节反复出现 ≥3 个年度波峰。适合提前布局，但不是第一次出现的需求。"),
    ("老词翻红仅标注", "长青老词翻红", "5 年均值落在 20–70，属于常年有搜索量的老词近期抬升。报告只标注，绝不当成首次爆发。"),
    ("新域名早鸟", None, "新注册且尚未解析，或已解析上线的工具向域名。未解析本身就是极早期立项信号。不把网页 title 里的大词当主词。"),
    ("同行新页面", None, "头部工具站 sitemap 相对上次运行的新增 URL（按 lastmod 倒序）。lastmod 只表示页面更新时间，不是关键词起量时间。"),
]


def _now_label() -> str:
    now = datetime.now(TZ)
    return now.strftime("%Y-%m-%d %H:%M") + " (Asia/Singapore)"


def _esc(s) -> str:
    return html.escape("" if s is None else str(s))


def _fmt_mean(v) -> str:
    if v is None:
        return "—"
    return f"{v:.2f}"


def evidence_bits(c: dict) -> list[str]:
    bits = [f"命中信源 {c.get('source_count')}/3：" + "、".join(c.get("sources") or [])]
    if c.get("has_5y"):
        onset = c.get('first_nonzero_week') or '—'
        if c.get('onset_censored'):
            onset = f"{onset}（已是 5 年窗口第一周，说明更早就有搜索量，不能当成首次出现日）"
        bits.append(
            f"5y 均值 {_fmt_mean(c.get('mean_5y'))}，峰值 {c.get('peak_5y')}，"
            f"非零周 {c.get('nonzero_weeks')}/{c.get('n_points')}，"
            f"首次非零周 {onset}，"
            f"近年峰值窗口最高 {c.get('recent_max')}，年度峰年数 {c.get('yearly_peaks')}"
        )
    for t in (c.get("trends") or [])[:4]:
        bits.append(
            f"Trends {t.get('timeframe')} / {t.get('relation')} / layer{t.get('layer')} "
            f"种子「{t.get('seed')}」→ {t.get('query')}（{t.get('formatted_value') or t.get('value')}）"
        )
    for d in (c.get("domains") or [])[:5]:
        extra = []
        if d.get("classification"):
            extra.append(d["classification"])
        if d.get("has_pricing"):
            extra.append("发现定价页 " + (d.get("pricing_url") or ""))
        if d.get("title") and d.get("classification") == "live":
            extra.append("title: " + d["title"][:80])
        bits.append("域名 " + d.get("domain", "") + (("（" + "；".join(extra) + "）") if extra else ""))
    for p in (c.get("pages") or [])[:4]:
        lm = p.get("lastmod") or "无 lastmod"
        bits.append(f"同行页面 {p.get('site')}: {p.get('url')}（lastmod={lm}，不作起量日）")
    return bits


def collect_report_items(
    classified: list[dict],
    domain_rows: list[dict],
    sitemap_new: list[dict],
    first_sitemap_run: bool,
) -> dict:
    """Split into five sections. Keyword sections require 5y data."""
    by_cls = {"纯血从零突发": [], "年度周期回潮": [], "长青老词翻红": []}
    used_terms = set()
    for c in classified:
        if c.get("pool") == "dropped":
            continue
        if not c.get("has_5y"):
            continue
        cls = c.get("class")
        if cls in by_cls:
            # assertion material: evergreen cannot be labelled first-breakout
            if cls == "长青老词翻红":
                assert c.get("mean_5y") is not None and c["mean_5y"] >= 20
            if cls == "纯血从零突发":
                assert c.get("mean_5y") is not None and c["mean_5y"] <= 2
                assert cls != "长青老词翻红"
            by_cls[cls].append(c)
            used_terms.add(c["term"])

    # Early-bird domains: unresolved first, then live with pricing, then live.
    early = []
    seen_d = set()
    for c in classified:
        for d in c.get("domains") or []:
            if d.get("domain") in seen_d:
                continue
            if d.get("classification") == "parked":
                continue
            seen_d.add(d["domain"])
            early.append({**d, "linked_term": c["term"], "pool": c.get("pool"), "has_5y": c.get("has_5y")})
    for d in domain_rows:
        if d.get("domain") in seen_d:
            continue
        if d.get("classification") == "parked":
            continue
        seen_d.add(d["domain"])
        early.append({**d, "linked_term": d.get("phrase") or "", "pool": "", "has_5y": False})

    def early_key(d):
        cls = d.get("classification")
        rank = 0 if cls == "unresolved" else (1 if d.get("has_pricing") else (2 if cls == "live" else 3))
        return (rank, -(d.get("score") or 0), d.get("domain") or "")

    early.sort(key=early_key)

    pages = sorted(
        sitemap_new,
        key=lambda p: (p.get("lastmod") or "", p.get("url") or ""),
        reverse=True,
    )
    return {
        "纯新词": by_cls["纯血从零突发"],
        "周期回潮": by_cls["年度周期回潮"],
        "老词翻红仅标注": by_cls["长青老词翻红"],
        "新域名早鸟": early,
        "同行新页面": pages,
        "first_sitemap_run": first_sitemap_run,
    }


def assert_no_fabrication(sections: dict) -> list[str]:
    warnings = []
    for c in sections["纯新词"]:
        if c.get("class") == "长青老词翻红" or (c.get("mean_5y") or 0) > 2:
            raise AssertionError(f"refusing to call {c['term']!r} a first-time breakout")
        if not c.get("has_5y"):
            raise AssertionError(f"{c['term']!r} entered 纯新词 without 5y data")
    for c in sections["老词翻红仅标注"]:
        if not c.get("has_5y"):
            raise AssertionError(f"{c['term']!r} entered evergreen section without 5y data")
    return warnings


def render_markdown(
    run_date: str,
    sections: dict,
    stats: list[dict],
    source_notes: dict,
) -> str:
    lines = []
    lines.append(f"# 出海新词雷达日报 {run_date}")
    lines.append("")
    lines.append(f"生成时间：{_now_label()}。所有数字来自本次跑出来的真实采集与 5 年 Trends 序列，没有补全或估算。")
    lines.append("")
    lines.append("## 采集摘要")
    lines.append("")
    for s in stats:
        note = f" — {s['note']}" if s.get("note") else ""
        lines.append(f"- {s['stage']}: **{s['count']}**{note}")
    lines.append("")
    # honest counts, no padding
    k_counts = {k: len(sections[k]) for k, _, _ in SECTION_DEFS if k in ("纯新词", "周期回潮", "老词翻红仅标注")}
    total_kw = sum(k_counts.values())
    lines.append(
        f"进入报告关键词板块（必须带 5 年数据）共 **{total_kw}** 条："
        + "，".join(f"{k} {v} 条" for k, v in k_counts.items())
        + "。未凑数，不够就不写满。"
    )
    if source_notes.get("trends_block"):
        lines.append("")
        lines.append(f"> Google Trends 异常：{source_notes['trends_block']}")
    lines.append("")
    for title, _cls, hint in SECTION_DEFS:
        items = sections[title]
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f"*{hint}*")
        lines.append("")
        if title == "同行新页面" and sections.get("first_sitemap_run"):
            lines.append("这是第一次拉这些站点的 sitemap，没有上一期快照可 diff，因此本日不把任何 URL 标成「今日新页面」。已将全量 URL 入库，下一期开始才能给增量。")
            lines.append("")
            continue
        if not items:
            lines.append("本日无条目。")
            lines.append("")
            continue
        if title == "新域名早鸟":
            for i, d in enumerate(items[:80], 1):
                pricing = ""
                if d.get("has_pricing"):
                    pricing = f"，定价页：{d.get('pricing_url')}"
                title_s = f"，title：{d.get('title')}" if d.get("title") and d.get("classification") == "live" else ""
                lines.append(
                    f"{i}. `{d.get('domain')}` — 词根「{d.get('phrase') or d.get('linked_term') or '—'}」，"
                    f"状态 **{d.get('classification')}**{pricing}{title_s}"
                )
            if len(items) > 80:
                lines.append(f"… 另有 {len(items)-80} 条已入库，报告只列前 80。")
            lines.append("")
            continue
        if title == "同行新页面":
            for i, p in enumerate(items[:80], 1):
                lines.append(
                    f"{i}. [{p.get('site')}] {p.get('url')}  "
                    f"slug：`{p.get('slug_phrase') or p.get('slug')}`  "
                    f"lastmod：{p.get('lastmod') or '（无）'}（不是起量日）"
                )
            if len(items) > 80:
                lines.append(f"… 另有 {len(items)-80} 条已入库，报告只列前 80。")
            lines.append("")
            continue
        for i, c in enumerate(items, 1):
            lines.append(f"### {i}. {c['term']}")
            lines.append("")
            if title == "老词翻红仅标注":
                lines.append("**这是长青老词，不是首次爆发。**")
                lines.append("")
            for b in evidence_bits(c):
                lines.append(f"- {b}")
            lines.append("")
    lines.append("## 信源说明")
    lines.append("")
    for k, v in (source_notes.get("details") or {}).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    return "\n".join(lines)


def render_html(run_date: str, md_text: str, sections: dict, stats: list[dict], source_notes: dict) -> str:
    k_counts = {k: len(sections[k]) for k, _, _ in SECTION_DEFS}
    cards = []
    for title, _cls, hint in SECTION_DEFS:
        items = sections[title]
        body = []
        if title == "同行新页面" and sections.get("first_sitemap_run"):
            body.append("<p class='empty'>第一次拉取 sitemap，没有上一期可对比，本日不标注新增页面。全量 URL 已入库。</p>")
        elif not items:
            body.append("<p class='empty'>本日无条目。</p>")
        elif title == "新域名早鸟":
            body.append("<ul class='list'>")
            for d in items[:80]:
                pricing = ""
                if d.get("has_pricing"):
                    pricing = f"<span class='tag price'>定价页</span> {_esc(d.get('pricing_url'))}"
                title_s = ""
                if d.get("title") and d.get("classification") == "live":
                    title_s = f"<div class='muted'>title：{_esc(d.get('title'))}</div>"
                cls = d.get("classification") or ""
                body.append(
                    "<li>"
                    f"<code>{_esc(d.get('domain'))}</code> "
                    f"<span class='tag { _esc(cls) }'>{_esc(cls)}</span> "
                    f"<span class='phrase'>{_esc(d.get('phrase') or d.get('linked_term'))}</span>"
                    f"{pricing}{title_s}"
                    "</li>"
                )
            body.append("</ul>")
            if len(items) > 80:
                body.append(f"<p class='muted'>另有 {len(items)-80} 条已入库。</p>")
        elif title == "同行新页面":
            body.append("<ul class='list'>")
            for p in items[:80]:
                body.append(
                    "<li>"
                    f"<span class='site'>{_esc(p.get('site'))}</span> "
                    f"<a href='{_esc(p.get('url'))}'>{_esc(p.get('url'))}</a>"
                    f"<div class='muted'>slug：{_esc(p.get('slug_phrase') or p.get('slug'))} · lastmod {_esc(p.get('lastmod') or '无')}（不是起量日）</div>"
                    "</li>"
                )
            body.append("</ul>")
            if len(items) > 80:
                body.append(f"<p class='muted'>另有 {len(items)-80} 条已入库。</p>")
        else:
            for c in items:
                ev = "".join(f"<li>{_esc(b)}</li>" for b in evidence_bits(c))
                warn = ""
                if title == "老词翻红仅标注":
                    warn = "<div class='warn'>这是长青老词，不是首次爆发。</div>"
                body.append(
                    "<article class='item'>"
                    f"<h3>{_esc(c['term'])}</h3>{warn}"
                    f"<ul class='ev'>{ev}</ul>"
                    "</article>"
                )
        cards.append(
            f"<section id='{_esc(title)}'>"
            f"<header><h2>{_esc(title)} <em>{k_counts[title]}</em></h2>"
            f"<p>{_esc(hint)}</p></header>"
            f"{''.join(body)}"
            "</section>"
        )
    stat_rows = "".join(
        f"<tr><th>{_esc(s['stage'])}</th><td>{_esc(s['count'])}</td><td>{_esc(s.get('note') or '')}</td></tr>"
        for s in stats
    )
    block = ""
    if source_notes.get("trends_block"):
        block = f"<aside class='alert'>{_esc(source_notes['trends_block'])}</aside>"
    details = "".join(
        f"<li><strong>{_esc(k)}</strong> — {_esc(v)}</li>"
        for k, v in (source_notes.get("details") or {}).items()
    )
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>出海新词雷达日报 { _esc(run_date) }</title>
<style>
  :root {{
    --ink: #1c1915;
    --muted: #6b645a;
    --paper: #f6f1e8;
    --card: #fffdf8;
    --line: #e2d8c8;
    --accent: #9c3b1e;
    --good: #1f6b4a;
    --warn: #8a4b12;
    --blue: #1e4a73;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font: 16px/1.65 "Iwanami Antique", "Source Han Serif SC", "Noto Serif SC", "Songti SC", Georgia, serif;
    color: var(--ink);
    background: var(--paper);
  }}
  header.hero {{
    padding: 48px 6vw 24px;
    border-bottom: 1px solid var(--line);
  }}
  header.hero p.kicker {{
    letter-spacing: 0.16em;
    text-transform: uppercase;
    font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif;
    font-size: 12px;
    color: var(--accent);
    margin: 0 0 8px;
  }}
  h1 {{ font-size: clamp(28px, 4vw, 44px); font-weight: 600; margin: 0 0 12px; }}
  .hero .meta {{ color: var(--muted); font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif; font-size: 14px; }}
  main {{ padding: 24px 6vw 80px; max-width: 1100px; }}
  table.stats {{ width: 100%; border-collapse: collapse; font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif; font-size: 14px; margin: 16px 0 32px; }}
  table.stats th {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); white-space: nowrap; }}
  table.stats td {{ padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }}
  section {{ background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 22px 24px; margin: 0 0 22px; }}
  section header h2 {{ margin: 0 0 8px; font-size: 22px; }}
  section header h2 em {{
    font-style: normal;
    font-family: "IBM Plex Sans", sans-serif;
    font-size: 13px;
    background: var(--ink);
    color: var(--paper);
    border-radius: 999px;
    padding: 1px 9px;
    margin-left: 8px;
    vertical-align: middle;
  }}
  section header p {{ margin: 0 0 16px; color: var(--muted); font-size: 14px; }}
  article.item {{ padding: 12px 0; border-top: 1px dashed var(--line); }}
  article.item h3 {{ margin: 0 0 8px; font-size: 18px; }}
  ul.ev, ul.list {{ margin: 0; padding-left: 18px; }}
  ul.ev li, ul.list li {{ margin: 0 0 6px; }}
  .empty, .muted {{ color: var(--muted); }}
  .warn {{ color: var(--warn); font-weight: 600; margin: 0 0 8px; font-family: "IBM Plex Sans", "Noto Sans SC", sans-serif; font-size: 13px; }}
  .alert {{ background: #f8e6d8; border: 1px solid #e2b48c; padding: 12px 16px; border-radius: 10px; margin: 12px 0 24px; }}
  code {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: 13px; background: #efe8dc; padding: 0 4px; border-radius: 4px; }}
  a {{ color: var(--blue); }}
  .tag {{ display: inline-block; font-family: "IBM Plex Sans", sans-serif; font-size: 11px; padding: 0 7px; border-radius: 999px; margin: 0 6px 0 4px; border: 1px solid var(--line); }}
  .tag.unresolved {{ background: #efe6c8; }}
  .tag.live {{ background: #d7eedf; }}
  .tag.price {{ background: #f3d9c8; }}
  .tag.resolved_no_http {{ background: #e8e4dc; }}
  .phrase {{ color: var(--muted); }}
  .site {{ font-family: "IBM Plex Sans", sans-serif; font-size: 12px; margin-right: 8px; color: var(--accent); }}
  footer {{ color: var(--muted); font-size: 13px; padding: 0 6vw 48px; }}
</style>
</head>
<body>
  <header class="hero">
    <p class="kicker">Xinci Radar · 出海新词日报</p>
    <h1>出海新词雷达 { _esc(run_date) }</h1>
    <p class="meta">生成于 {_esc(_now_label())}。数字全部来自本次采集，未凑条、未编造 5 年数据。长青词只会标注，不会写成首次爆发。</p>
  </header>
  <main>
    {block}
    <table class="stats">
      <thead><tr><th>阶段</th><th>数量</th><th>说明</th></tr></thead>
      <tbody>{stat_rows}</tbody>
    </table>
    {''.join(cards)}
    <section>
      <header><h2>信源说明</h2></header>
      <ul class="list">{details}</ul>
    </section>
  </main>
  <footer>报告由本机脚本生成，路径见同目录 Markdown。Timezone: Asia/Singapore。</footer>
</body>
</html>
"""


def write_reports(run_date: str, sections: dict, stats: list[dict], source_notes: dict) -> tuple[Path, Path]:
    assert_no_fabrication(sections)
    REPORTS.mkdir(parents=True, exist_ok=True)
    md = render_markdown(run_date, sections, stats, source_notes)
    html_doc = render_html(run_date, md, sections, stats, source_notes)
    md_path = REPORTS / f"{run_date}.md"
    html_path = REPORTS / f"{run_date}.html"
    md_path.write_text(md, encoding="utf-8")
    html_path.write_text(html_doc, encoding="utf-8")
    return md_path, html_path
