#!/usr/bin/env python3
"""
Update TRACK_RECORD.md — a daily, public receipt of how the engine's own
morning views actually scored (resolved), straight from the live public API.

Each row = ONE past date's morning views, scored on the record after their
window closed: hit / miss / invalidated / unscorable — warts and all.

⚠ Method (S110 fix): earlier this read the *latest* briefing, whose views are
freshly issued and always "not yet scored" — meaningless. Now it reads a
*resolved* past date via /public/briefing?date=YYYY-MM-DD and backfills the
recent resolved days, so the ledger shows real outcomes, not empty snapshots.

Requires DECKER_API_KEY (GitHub secret) — the full daily briefing (every symbol).
Run by .github/workflows/track-record.yml on a daily cron. Pure stdlib.

    DECKER_API_KEY=... python scripts/update_track_record.py
"""
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone

API = "https://api.decker-ai.com/api/v1"
UA = {"Accept": "application/json", "User-Agent": "decker-track-record/1.0"}
LEDGER = "TRACK_RECORD.md"
MAX_ROWS = 120          # ~4 months of daily rows
BACKFILL_DAYS = 7       # each run fills any missing resolved day in this window

# view outcome, plain-English (the arc, not just the state)
_OUTCOME = {
    "hit": "target hit",
    "miss": "held / no target",
    "invalidated": "view changed",
    "unscorable": "no candle",
}


def _get(path: str, key: str | None = None) -> dict:
    headers = dict(UA)
    if key:
        headers["X-API-Key"] = key
    req = urllib.request.Request(f"{API}{path}", headers=headers)
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def _tally(verdicts) -> str:
    counts: dict[str, int] = {}
    for v in verdicts:
        if v:
            counts[v] = counts.get(v, 0) + 1
    if not counts:
        return "— (not yet scored)"
    order = ["hit", "miss", "invalidated", "unscorable"]
    parts = [f"{k} {counts[k]}" for k in order if k in counts]
    parts += [f"{k} {n}" for k, n in counts.items() if k not in order]
    return " · ".join(parts)


def build_row(date: str, key: str) -> str | None:
    """Row for a *resolved* date = that date's morning views, scored.
    Returns None if no morning briefing that date."""
    d = _get(f"/public/briefing?date={date}", key)
    if not d.get("date"):
        return None
    syms = d.get("symbols", []) or []          # endpoint already excludes tf_view/rerun
    if not syms:
        return None
    scope = f"{len(syms)} views"
    scorecard = _tally([s.get("verdict") for s in syms if s.get("verdict")])
    resolved = [s for s in syms if s.get("verdict") and s.get("verdict") != "unscorable"]
    sample = ", ".join(
        f"{s.get('symbol')} {s.get('direction')} → {_OUTCOME.get(s.get('verdict'), s.get('verdict'))}"
        for s in resolved[:3]
    ) or "—"
    return f"| {date} | {scope} | {scorecard} | {sample} |"


def _row_date(row: str) -> str:
    return row.split("|")[1].strip()


HEADER = (
    "# Track record — the engine scores its own views, daily\n\n"
    "Most signal products show you the wins. This file is the opposite: a\n"
    "GitHub Action appends **one row per resolved day**, straight from the live\n"
    "public API — no cherry-picking, no editing. Each row = that morning's views,\n"
    "scored on the record after their window closed. The repo itself is the\n"
    "receipt that the engine runs, deterministically, in the open.\n\n"
    "> `hit` = view reached its target · `miss` = held, target not reached · "
    "`invalidated` = view changed (invalidation line touched) · `unscorable` = "
    "no candle to score. Full daily briefing + per-view tracking: "
    "[decker-ai.com/briefing](https://decker-ai.com/briefing).\n\n"
    "| Date (UTC) | Scope | Scorecard (hit · miss · invalidated) | Sample views (outcome) |\n"
    "|------------|-------|--------------------------------------|------------------------|\n"
)


def main() -> None:
    key = os.environ.get("DECKER_API_KEY")
    if not key:
        raise SystemExit("DECKER_API_KEY required — the track record scores every symbol's resolved views.")

    today = datetime.now(timezone.utc).date()

    old_rows = []
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("| 20") and "| Date" not in s:
                    old_rows.append(s)

    # Build fresh rows for recent *resolved* days (lag ≥1 = window closed; today skipped = unresolved).
    fresh: dict[str, str] = {}
    for lag in range(1, BACKFILL_DAYS + 1):
        d = (today - timedelta(days=lag)).isoformat()
        row = build_row(d, key)
        if row and "not yet scored" not in row:   # only stamp resolved days
            fresh[d] = row

    # Fresh (resolved) rows replace any stale same-date row; keep older rows as-is.
    merged = list(fresh.values()) + [r for r in old_rows if _row_date(r) not in fresh]
    # dedup by date, newest first, cap
    seen, out = set(), []
    for r in sorted(merged, key=_row_date, reverse=True):
        dt = _row_date(r)
        if dt in seen:
            continue
        seen.add(dt)
        out.append(r)
    out = out[:MAX_ROWS]

    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write(HEADER + "\n".join(out) + "\n\n_For information only. Not investment advice._\n")

    print(f"track record updated: {len(fresh)} resolved rows refreshed, {len(out)} total")


if __name__ == "__main__":
    main()
