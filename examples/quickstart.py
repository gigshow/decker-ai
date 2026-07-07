#!/usr/bin/env python3
"""
Decker AI — 60-second quickstart. No signup, no API key.

Hits the public demo endpoint and prints the composed market-state view
(the same card the daily briefing sends). Pure stdlib — no dependencies.

    python quickstart.py
"""
import json
import urllib.request

# Public demo: BTCUSDT only, ~10 requests / IP / day, no auth.
DEMO_URL = "https://api.decker-ai.com/api/v1/public/demo"
HEADERS = {"Accept": "application/json", "User-Agent": "decker-quickstart/1.0"}


def get_demo_view() -> dict:
    req = urllib.request.Request(DEMO_URL, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


def main() -> None:
    v = get_demo_view()

    print(f"\n{v['name']}  ·  {v['timeframe']}  ·  state={v['c_state']}  dir={v['direction']}")
    print("-" * 56)
    for line in v.get("compact_lines", []):
        print(f"  {line}")
    print("-" * 56)
    print(f"  ref_price    : {v['ref_price']}")
    print(f"  wait_target  : {v['wait_target']}")
    print(f"  invalidation : {v['invalidation']}")

    # Receipts — the engine scores its own past calls, hits and misses alike.
    print("\n  recent verdicts (receipts):")
    for r in v.get("verdict_recent", []):
        print(f"    {r['briefing_date']}  {r['slot']:<8} {r['timeframe']:<3} ->  {r['verdict']}")

    # Provenance — every read traces to the exact rulebook contract.
    print(f"\n  provenance : {v['provenance']['contract']}")
    print(f"  requests left today : {v['_demo']['rate_limit_remaining']}\n")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Next step — with a free API key (decker-ai.com -> Settings -> API Keys,
# or Telegram @deckerclawbot -> /apikey) you get any symbol + timeframe:
#
#   GET https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h
#   header:  X-API-Key: dk_live_xxx
#
# For information only. Not investment advice.
# ---------------------------------------------------------------------------
