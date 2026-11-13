from __future__ import annotations

import re
from datetime import datetime
from urllib.parse import urlparse
from xml.etree import ElementTree as ET

import requests
import yaml

from radar.paths import SITES_YAML
from radar.domains import USER_AGENT
from radar.textutil import phrase_from_words, tokenize

LANG_PREFIX = re.compile(
    r"^/(?:es|fr|de|pt|pt-br|pt-pt|ja|zh|zh-cn|zh-tw|zh-hk|it|nl|ko|ru|ar|tr|pl|"
    r"sv|da|fi|id|th|vi|uk|he|cs|ro|hu|el|nb|nn|no|sk|bg|hr|sr|sl|lt|lv|et|"
    r"ms|hi|bn|ta|te|fa|fil|tl|ca|eu|gl|vi-vn|es-\w{2}|fr-\w{2}|de-\w{2}|"
    r"pt-\w{2}|it-\w{2}|nl-\w{2}|zh-\w{2})(?=/|$)",
    re.I,
)
LANG_INFIX = re.compile(
    r"/(?:es|fr|de|pt|ja|zh|it|nl|ko|ru|ar|tr|pl)/(?=[a-z0-9\-])",
    re.I,
)

SKIP_NAME_RE = re.compile(r"(image|video|news|blog-?index|author|tag|category|product-image)", re.I)

MAX_URLS_PER_SITE = 8000
MAX_SITEMAP_DOCS = 40


def load_sites() -> list[dict]:
    data = yaml.safe_load(SITES_YAML.read_text(encoding="utf-8"))
    return data["sites"]


def _strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1] if "}" in tag else tag


def _parse_xml(content: bytes) -> ET.Element | None:
    try:
        return ET.fromstring(content)
    except ET.ParseError:
        # sometimes trailing junk
        try:
            start = content.find(b"<")
            return ET.fromstring(content[start:])
        except ET.ParseError:
            return None


def fetch_bytes(sess: requests.Session, url: str) -> tuple[int | None, bytes, str]:
    try:
        r = sess.get(url, timeout=25, allow_redirects=True)
        return r.status_code, r.content, r.url
    except requests.RequestException as e:
        return None, str(e).encode(), url


def iter_sitemap_docs(sess: requests.Session, start_urls: list[str]) -> list[tuple[str, ET.Element]]:
    seen = set()
    queue = list(start_urls)
    docs = []
    while queue and len(docs) < MAX_SITEMAP_DOCS:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        if SKIP_NAME_RE.search(urlparse(url).path or ""):
            continue
        status, content, final = fetch_bytes(sess, url)
        if not status or status >= 400 or not content.startswith(b"<") and b"<urlset" not in content and b"<sitemapindex" not in content:
            continue
        root = _parse_xml(content)
        if root is None:
            continue
        kind = _strip_ns(root.tag).lower()
        if kind == "sitemapindex":
            for sm in root:
                if _strip_ns(sm.tag).lower() != "sitemap":
                    continue
                loc = ""
                for child in sm:
                    if _strip_ns(child.tag).lower() == "loc" and child.text:
                        loc = child.text.strip()
                if loc and loc not in seen:
                    queue.append(loc)
        else:
            docs.append((final, root))
    return docs


def lang_stripped_url(url: str) -> tuple[str, bool]:
    p = urlparse(url)
    path = p.path or "/"
    new_path, n = LANG_PREFIX.subn("/", path, count=1)
    stripped = n > 0
    if not stripped:
        new_path2, n2 = LANG_INFIX.subn("/", path, count=1)
        if n2:
            new_path = new_path2
            stripped = True
    new_path = re.sub(r"/{2,}", "/", new_path)
    rebuilt = p._replace(path=new_path, query="", fragment="").geturl()
    return rebuilt, stripped


def slug_phrase(url: str) -> tuple[str, str]:
    path = urlparse(url).path.rstrip("/")
    parts = [x for x in path.split("/") if x]
    # skip file-like last segments with extensions other than none
    while parts and re.search(r"\.(xml|html?|php|asp|json)$", parts[-1], re.I):
        parts.pop()
    if not parts:
        return "", ""
    slug = parts[-1]
    # if last is a thin token (digits, 'blog'), include previous
    if re.fullmatch(r"\d+", slug) or slug.lower() in {"index", "page", "blog", "post", "docs"}:
        if len(parts) >= 2:
            slug = parts[-2] + " " + slug
    phrase = " ".join(tokenize(slug.replace("-", " ")))
    return slug, phrase


def harvest(run_date: str) -> tuple[list[dict], dict]:
    sess = requests.Session()
    sess.headers["User-Agent"] = USER_AGENT
    sess.headers["Accept"] = "application/xml,text/xml,application/xhtml+xml,*/*"
    sites = load_sites()
    rows = []
    notes = {}
    for site in sites:
        name = site["name"]
        start = list(site.get("sitemaps") or [])
        docs = iter_sitemap_docs(sess, start)
        urls = []
        seen_canon = set()
        for _final, root in docs:
            for node in root:
                if _strip_ns(node.tag).lower() != "url":
                    continue
                loc, lastmod = "", ""
                for child in node:
                    tag = _strip_ns(child.tag).lower()
                    if tag == "loc" and child.text:
                        loc = child.text.strip()
                    elif tag == "lastmod" and child.text:
                        lastmod = child.text.strip()
                if not loc or not loc.startswith("http"):
                    continue
                canon, stripped = lang_stripped_url(loc)
                if canon in seen_canon:
                    continue
                seen_canon.add(canon)
                slug, phrase = slug_phrase(canon)
                urls.append(
                    {
                        "run_date": run_date,
                        "site": name,
                        "url": canon,
                        "lastmod": lastmod,
                        "slug": slug,
                        "slug_phrase": phrase,
                        "lang_stripped": 1 if stripped else 0,
                        "is_new": 0,
                    }
                )
                if len(urls) >= MAX_URLS_PER_SITE:
                    break
            if len(urls) >= MAX_URLS_PER_SITE:
                break
        notes[name] = {"docs": len(docs), "urls": len(urls), "starts": start}
        rows.extend(urls)
    return rows, notes


def mark_new(rows: list[dict], previous_urls: set[str]) -> list[dict]:
    if not previous_urls:
        # First run: cannot know what is new vs historical. Mark nothing as
        # "new today"; still store all URLs so tomorrow can diff.
        for r in rows:
            r["is_new"] = 0
        return rows
    for r in rows:
        r["is_new"] = 1 if r["url"] not in previous_urls else 0
    return rows


def lastmod_sort_key(value: str) -> str:
    if not value:
        return ""
    return value
