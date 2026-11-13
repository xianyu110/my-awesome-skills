from __future__ import annotations

import base64
import io
import re
import socket
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from radar.paths import CACHE
from radar.textutil import extract_matching_roots, load_roots, phrase_from_words, segment_sld

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

JUNK_WORDS = re.compile(
    r"(porn|xxx|sexcam|casino|gambling|bet365|pharmacy|viagra|loan-?now|"
    r"crypto-?pump|airdrop-?claim)",
    re.I,
)

PARKED_MARKERS = (
    "domain is for sale",
    "buy this domain",
    "this domain is listed",
    "parked domain",
    "domain parking",
    "sedoparking",
    "hugedomains",
    "afternic",
    "dan.com",
    "godaddy.com/domainsearch",
    "sedo.com",
    "undeveloped.com",
    "bodis.com",
    "parkingcrew",
    "is for sale on",
    "inquire about this domain",
    "this webpage is parked",
    "default web page",
    "website coming soon",
)

PRICING_PATH_RE = re.compile(
    r"/(pricing|plans?|subscribe|subscription|checkout|buy|upgrade)(/|$|\?)",
    re.I,
)
PRICING_TEXT_RE = re.compile(
    r"\b(pricing|plans? & pricing|start( for)? free|subscribe now|"
    r"per month|/mo\b|buy now|pro plan|premium plan)\b",
    re.I,
)

INTERESTING_TLDS = {
    "com", "io", "ai", "app", "dev", "co", "net", "org", "xyz", "so",
    "gg", "me", "info", "pro", "studio", "tools", "tech", "online", "site",
}


def _whoisds_url(day: str) -> str:
    infix = base64.b64encode(f"{day}.zip".encode()).decode()[:-1]
    return f"https://whoisds.com/whois-database/newly-registered-domains/{infix}/nrd"


def download_whoisds(run_date: str, max_lookback: int = 4) -> tuple[str, list[str], str]:
    """Return (package_date, domains, note). Prefer the newest free package."""
    CACHE.mkdir(parents=True, exist_ok=True)
    sess = requests.Session()
    sess.headers["User-Agent"] = USER_AGENT
    errors = []
    # Free list is typically published for yesterday (UTC).
    today = datetime.now(timezone.utc).date()
    for i in range(1, max_lookback + 1):
        day = (today - timedelta(days=i)).isoformat()
        dest = CACHE / f"nrd-{day}.txt"
        if dest.exists() and dest.stat().st_size > 1000:
            domains = [l.strip().lower() for l in dest.read_text(errors="replace").splitlines() if l.strip()]
            return day, domains, f"cache hit {dest.name} n={len(domains)}"
        url = _whoisds_url(day)
        try:
            r = sess.get(url, timeout=90)
            if r.status_code != 200 or len(r.content) < 1000:
                errors.append(f"{day}: HTTP {r.status_code} len={len(r.content)}")
                continue
            z = zipfile.ZipFile(io.BytesIO(r.content))
            name = z.namelist()[0]
            text = z.read(name).decode("utf-8", "replace")
            dest.write_text(text, encoding="utf-8")
            domains = [l.strip().lower() for l in text.splitlines() if l.strip()]
            return day, domains, f"downloaded {url} n={len(domains)}"
        except Exception as e:
            errors.append(f"{day}: {type(e).__name__}: {e}")
    raise RuntimeError("WhoisDS download failed: " + " | ".join(errors))


def split_domain(domain: str) -> tuple[str, str]:
    host = domain.lower().strip().rstrip(".")
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) < 2:
        return host, ""
    # cheap eTLD: co.uk, com.au etc.
    if len(parts) >= 3 and parts[-2] in {"co", "com", "net", "org", "ac"} and len(parts[-1]) == 2:
        sld, tld = parts[-3], ".".join(parts[-2:])
    else:
        sld, tld = parts[-2], parts[-1]
    return sld, tld


def is_junk_domain(domain: str) -> bool | str:
    sld, tld = split_domain(domain)
    if not sld or not tld:
        return "malformed"
    if sld.startswith("xn--") or domain.startswith("xn--"):
        return "punycode"
    if JUNK_WORDS.search(domain):
        return "adult_spam"
    if len(sld) < 4:
        return "too_short"
    if len(sld) > 40:
        return "too_long"
    if re.fullmatch(r"[0-9]+", sld):
        return "numeric"
    if sld.count("-") >= 4:
        return "hyphen_spam"
    letters = re.sub(r"[^a-z]", "", sld)
    digits = re.sub(r"[^0-9]", "", sld)
    if letters and len(digits) >= 5 and len(digits) >= len(letters):
        return "digit_heavy"
    vowels = len(re.findall(r"[aeiou]", letters))
    if letters and len(letters) >= 8 and vowels <= 1:
        return "no_vowels"
    # high entropy / random consonant soup
    if letters and len(letters) >= 12:
        unique = len(set(letters))
        if unique / len(letters) > 0.85 and vowels / len(letters) < 0.25:
            return "random"
    return False


def score_domain(sld: str, words: list[str], roots: list[str]) -> int:
    score = 0
    if roots:
        score += 30 + 8 * len(roots)
    content = [w for w in words if len(w) >= 3]
    if len(content) >= 2:
        score += 10 + 2 * min(len(content), 5)
    # penalize single leftover crumbs
    if any(len(w) == 1 for w in words):
        score -= 2
    return score


def filter_interesting(domains: Iterable[str], cap: int = 800) -> list[dict]:
    rootset = load_roots()["set"]
    kept = []
    for d in domains:
        reason = is_junk_domain(d)
        if reason:
            continue
        sld, tld = split_domain(d)
        words = segment_sld(sld)
        roots = extract_matching_roots(sld, words)
        score = score_domain(sld, words, roots)
        if not roots and (tld not in INTERESTING_TLDS or len([w for w in words if len(w) >= 4]) < 2):
            continue
        if score < 10:
            continue
        kept.append(
            {
                "domain": d,
                "sld": sld,
                "tld": tld,
                "words": words,
                "roots": roots,
                "phrase": phrase_from_words(words),
                "score": score,
            }
        )
    kept.sort(key=lambda x: (-x["score"], x["domain"]))
    # unique phrases prefer higher score
    return kept[:cap]


def _dns_ok(host: str, timeout: float = 3.0) -> bool:
    old = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        socket.getaddrinfo(host, 443)
        return True
    except OSError:
        try:
            socket.getaddrinfo(host, 80)
            return True
        except OSError:
            return False
    finally:
        socket.setdefaulttimeout(old)


def _looks_parked(html: str, final_url: str, title: str) -> bool:
    blob = f"{title} {final_url} {html[:8000]}".lower()
    return any(m in blob for m in PARKED_MARKERS)


def _find_pricing(html: str, final_url: str) -> tuple[bool, str | None]:
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        href = a.get("href", "")
        text = a.get_text(" ", strip=True)
        if PRICING_PATH_RE.search(href) or PRICING_TEXT_RE.search(text or ""):
            return True, urljoin(final_url, href)
    if PRICING_TEXT_RE.search(soup.get_text(" ", strip=True)[:6000]):
        return True, final_url
    return False, None


def _meta_desc(soup: BeautifulSoup) -> str:
    for key in ("description", "og:description"):
        tag = soup.find("meta", attrs={"name": key}) or soup.find("meta", attrs={"property": key})
        if tag and tag.get("content"):
            return tag["content"].strip()[:400]
    return ""


def probe_one(domain: str, timeout: float = 8.0) -> dict:
    result = {
        "domain": domain,
        "dns_status": "unresolved",
        "http_status": None,
        "classification": "unresolved",
        "title": "",
        "description": "",
        "has_pricing": 0,
        "pricing_url": "",
        "final_url": "",
    }
    if not _dns_ok(domain):
        return result
    result["dns_status"] = "resolved"
    sess_headers = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}
    html = ""
    final = ""
    status = None
    for scheme in ("https", "http"):
        try:
            r = requests.get(
                f"{scheme}://{domain}/",
                headers=sess_headers,
                timeout=(3.0, timeout),
                allow_redirects=True,
                stream=True,
            )
            status = r.status_code
            final = r.url
            raw = b""
            for chunk in r.iter_content(8192):
                raw += chunk
                if len(raw) >= 120_000:
                    break
            r.close()
            html = raw.decode(r.encoding or "utf-8", "replace")
            if status and status < 500:
                break
        except requests.RequestException:
            continue
    result["http_status"] = status
    result["final_url"] = final
    if not html:
        result["classification"] = "resolved_no_http"
        return result
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.get_text(" ", strip=True) if soup.title else "")[:250]
    result["title"] = title
    result["description"] = _meta_desc(soup)
    if _looks_parked(html, final or "", title):
        result["classification"] = "parked"
        return result
    has, purl = _find_pricing(html, final or f"https://{domain}/")
    result["has_pricing"] = 1 if has else 0
    result["pricing_url"] = purl or ""
    result["classification"] = "live"
    return result


def probe_many(domains: list[str], workers: int = 24, cap: int = 350) -> list[dict]:
    targets = domains[:cap]
    out = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(probe_one, d): d for d in targets}
        for fut in as_completed(futs):
            try:
                out.append(fut.result())
            except Exception as e:
                out.append(
                    {
                        "domain": futs[fut],
                        "dns_status": "error",
                        "http_status": None,
                        "classification": "error",
                        "title": "",
                        "description": str(e)[:200],
                        "has_pricing": 0,
                        "pricing_url": "",
                        "final_url": "",
                    }
                )
    return out
