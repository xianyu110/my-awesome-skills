from __future__ import annotations

import json
import statistics
from datetime import date, datetime, timedelta, timezone

from radar.trends import TrendsClient, TrendsError


def _week_start_iso(point: dict) -> str | None:
    t = point.get("time")
    if t:
        try:
            dt = datetime.fromtimestamp(int(t), tz=timezone.utc)
            return dt.date().isoformat()
        except (ValueError, TypeError, OSError):
            pass
    return point.get("week_label")


def classify_series(points: list[dict]) -> dict:
    """Compute 5y stats over the full ~262-week window.

    Weeks with has_data=false are treated as 0 interest for the 底盘均值.
    Averaging only the sparse non-zero weeks would inflate old-word means.
    """
    if not points:
        return {
            "n_points": 0,
            "mean": None,
            "peak": None,
            "nonzero_weeks": None,
            "first_nonzero_week": None,
            "onset_censored": False,
            "yearly_peaks": 0,
            "recent_max": None,
            "class": None,
            "ok": False,
            "reason": "empty series",
        }
    values = []
    for p in points:
        if p.get("is_partial"):
            continue
        if p.get("has_data") and p.get("value") is not None:
            values.append(int(p["value"]))
        else:
            values.append(0)
    n = len(values)
    mean = float(sum(values) / n) if n else 0.0
    peak = int(max(values)) if values else 0
    nonzero = sum(1 for v in values if v > 0)
    first = None
    for p in points:
        if p.get("is_partial"):
            continue
        if p.get("has_data") and (p.get("value") or 0) > 0:
            first = _week_start_iso(p)
            break
    window_start = _week_start_iso(points[0]) if points else None
    onset_censored = bool(first and window_start and first == window_start)

    recent = points[-8:]
    recent_vals = []
    for p in recent:
        if p.get("has_data") and p.get("value") is not None:
            recent_vals.append(int(p["value"]))
        else:
            recent_vals.append(0)
    recent_max = max(recent_vals) if recent_vals else 0

    yearly_peaks = count_yearly_peaks(points)
    recent_spike = recent_max >= 40 and recent_max >= max(peak * 0.5, 40)
    onset_recent = False
    if first:
        try:
            onset_recent = date.fromisoformat(first) >= (date.today() - timedelta(days=548))
        except ValueError:
            onset_recent = False

    cls = "other"
    # 纯血: low 5y floor, recent onset (within ~18 months), and a real (non-partial-only) lift.
    if mean <= 2 and nonzero >= 1 and onset_recent and yearly_peaks < 3 and (recent_spike or recent_max >= 20):
        cls = "纯血从零突发"
    elif yearly_peaks >= 3:
        cls = "年度周期回潮"
    elif 20 <= mean <= 70:
        cls = "长青老词翻红"

    return {
        "n_points": len(points),
        "mean": round(mean, 3),
        "peak": peak,
        "nonzero_weeks": nonzero,
        "first_nonzero_week": first,
        "onset_censored": onset_censored,
        "yearly_peaks": yearly_peaks,
        "recent_max": recent_max,
        "class": cls,
        "ok": len(points) >= 200,
        "reason": "" if len(points) >= 200 else f"only {len(points)} weekly points, need ~262",
    }


def count_yearly_peaks(points: list[dict]) -> int:
    """Count distinct years that show a peak in a recurring week-of-year window."""
    series = []
    for p in points:
        if p.get("is_partial") or not p.get("has_data") or p.get("value") is None or not p.get("time"):
            continue
        try:
            dt = datetime.fromtimestamp(int(p["time"]), tz=timezone.utc)
        except (ValueError, TypeError, OSError):
            continue
        series.append((dt, int(p["value"])))
    if len(series) < 80:
        return 0
    values = [v for _, v in series]
    # threshold relative to the series
    try:
        med = statistics.median(values)
    except statistics.StatisticsError:
        med = 0
    mx = max(values) if values else 0
    if mx < 15:
        return 0
    thresh = max(15.0, med * 2.0, mx * 0.35)
    # local maxima in a ±3 week window
    peaks = []  # (year, week_of_year, value)
    for i, (dt, v) in enumerate(series):
        if v < thresh:
            continue
        window = [series[j][1] for j in range(max(0, i - 3), min(len(series), i + 4))]
        if v >= max(window):
            peaks.append((dt.isocalendar().year, dt.isocalendar().week, v))
    if not peaks:
        return 0
    # cluster by week-of-year (circular)
    best = 0
    for week in range(1, 54):
        years = set()
        for y, w, _ in peaks:
            dw = min(abs(w - week), 53 - abs(w - week))
            if dw <= 4:
                years.add(y)
        best = max(best, len(years))
    return best


def fetch_and_classify(client: TrendsClient, term: str) -> dict:
    raw = client.series_5y(term)
    stats = classify_series(raw["points"])
    stats["term"] = term
    stats["weekly"] = raw["points"]
    return stats
