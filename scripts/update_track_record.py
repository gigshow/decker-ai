#!/usr/bin/env python3
"""
Update TRACK_RECORD.md with today's engine reading — the repo stamps a daily,
public entry so the ledger is alive, not a screenshot.

No dependencies, no key needed: reads the public BTCUSDT demo. If a
DECKER_API_KEY env var is present, also pulls the multi-symbol briefing verdicts
(hits / misses) for a richer scorecard.

Run by .github/workflows/track-record.yml on a daily cron.

    python scripts/update_track_record.py
"""
import json
import os
import urllib.request
from datetime import datetime, timezone

API = "https://api.decker-ai.com/api/v1"
HEADERS = {"Accept": "application/json", "User-Agent": "decker-track-record/1.0"}
LEDGER = "TRACK_RECORD.md"
MAX_ROWS = 120  # keep the table to ~4 months of daily rows


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def today_row() -> str:
    d = _get(f"{API}/public/demo")
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sym = d.get("name") or d.get("symbol", "BTCUSDT")
    tf = d.get("timeframe", "?")
    state = d.get("c_state", "?")
    direction = d.get("direction", "?")
    ref = d.get("ref_price", "?")

    # Recent verdicts (hits / misses) — from demo, or richer if a key is set.
    verdicts = d.get("verdict_recent", []) or []
    key = os.environ.get("DECKER_API_KEY")
    if key:
        try:
            hdr = dict(HEADERS, **{"X-API-Key": key})
            req = urllib.request.Request(f"{API}/public/signals/{sym}/latest?timeframe={tf}", headers=hdr)
            with urllib.request.urlopen(req, timeout=20) as r:
                extra = json.load(r)
            verdicts = extra.get("verdict_recent", verdicts) or verdicts
        except Exception:
            pass

    if verdicts:
        counts = {}
        for v in verdicts:
            counts[v.get("verdict", "?")] = counts.get(v.get("verdict", "?"), 0) + 1
        vsum = " · ".join(f"{k} {n}" for k, n in sorted(counts.items()))
    else:
        vsum = "—"

    return f"| {date} | {sym} {tf} | `{state}` | {direction} | {ref} | {vsum} |"


def main() -> None:
    row = today_row()
    date = row.split("|")[1].strip()

    header = (
        "# Track record — the engine stamps its own reading, daily\n\n"
        "Most signal products show you the wins. This file is the opposite: a\n"
        "GitHub Action appends **one row every day**, straight from the live public\n"
        "API — no cherry-picking, no editing. The repo itself is the receipt that\n"
        "the engine runs, deterministically, in the open.\n\n"
        "> `verdict` = how a past briefing view scored the evening it was due — "
        "`hit` / `miss` / `invalidated`, on the record. Full daily briefing + "
        "self-scoring: [decker-ai.com/briefing](https://decker-ai.com/briefing).\n\n"
        "| Date (UTC) | Read | State | Dir | Ref price | Recent verdicts |\n"
        "|------------|------|-------|-----|-----------|-----------------|\n"
    )

    rows = []
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("| 20") and "| Date" not in s:  # a data row
                    rows.append(s)

    # De-dup today (idempotent re-runs), newest first, capped.
    rows = [r for r in rows if not r.startswith(f"| {date} ")]
    rows.insert(0, row)
    rows = rows[:MAX_ROWS]

    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(rows) + "\n\n_For information only. Not investment advice._\n")

    print(f"track record updated: {date} — {len(rows)} rows")


if __name__ == "__main__":
    main()
