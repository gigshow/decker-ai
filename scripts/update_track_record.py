#!/usr/bin/env python3
"""
Update TRACK_RECORD.md with today's scorecard — the repo stamps a daily, public
entry so the ledger is alive, not a screenshot.

- No key: reads the public BTCUSDT demo (single symbol).
- With DECKER_API_KEY: reads the full daily briefing (every symbol) and tallies
  how the engine's own views scored — hit / miss / invalidated, across the board.

Run by .github/workflows/track-record.yml on a daily cron. Pure stdlib.

    python scripts/update_track_record.py
"""
import json
import os
import urllib.request
from datetime import datetime, timezone

API = "https://api.decker-ai.com/api/v1"
UA = {"Accept": "application/json", "User-Agent": "decker-track-record/1.0"}
LEDGER = "TRACK_RECORD.md"
MAX_ROWS = 120  # ~4 months of daily rows


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
    order = ["hit", "miss", "invalidated"]
    parts = [f"{k} {counts[k]}" for k in order if k in counts]
    parts += [f"{k} {n}" for k, n in counts.items() if k not in order]
    return " · ".join(parts)


def build_row(date: str) -> str:
    key = os.environ.get("DECKER_API_KEY")
    if key:
        d = _get("/public/briefing", key)
        syms = d.get("symbols", []) or []
        scored = [s.get("verdict") for s in syms if s.get("verdict")]
        scope = f"{len(syms)} symbols"
        scorecard = _tally(scored)
        # a couple of live states as a sample
        sample = ", ".join(
            f"{s.get('symbol')} `{s.get('c_state')}`" for s in syms[:3]
        ) or "—"
    else:
        d = _get("/public/demo")
        scope = f"{d.get('name', 'BTC')} {d.get('timeframe', '')} (demo)".strip()
        scorecard = _tally([v.get("verdict") for v in d.get("verdict_recent", []) or []])
        sample = f"`{d.get('c_state')}` {d.get('direction')} · ref {d.get('ref_price')}"
    return f"| {date} | {scope} | {scorecard} | {sample} |"


def main() -> None:
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = build_row(date)

    header = (
        "# Track record — the engine scores its own views, daily\n\n"
        "Most signal products show you the wins. This file is the opposite: a\n"
        "GitHub Action appends **one row every day**, straight from the live public\n"
        "API — no cherry-picking, no editing. The repo itself is the receipt that\n"
        "the engine runs, deterministically, in the open.\n\n"
        "> `hit` / `miss` / `invalidated` = how each morning view scored the evening "
        "it was due, on the record. Full daily briefing + self-scoring: "
        "[decker-ai.com/briefing](https://decker-ai.com/briefing).\n\n"
        "| Date (UTC) | Scope | Scorecard (hit · miss · invalidated) | Sample states |\n"
        "|------------|-------|--------------------------------------|---------------|\n"
    )

    rows = []
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if s.startswith("| 20") and "| Date" not in s:
                    rows.append(s)

    rows = [r for r in rows if not r.startswith(f"| {date} ")]  # idempotent
    rows.insert(0, row)
    rows = rows[:MAX_ROWS]

    with open(LEDGER, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(rows) + "\n\n_For information only. Not investment advice._\n")

    print(f"track record updated: {date} — {len(rows)} rows")


if __name__ == "__main__":
    main()
