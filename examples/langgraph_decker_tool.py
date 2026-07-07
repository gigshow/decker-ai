#!/usr/bin/env python3
"""
Decker as a tool for a multi-agent crew (LangChain / LangGraph / AutoGen).

The trend is 5 LLM analysts debating a chart. The problem: they each
re-derive market structure from raw candles, every prompt, non-reproducibly.

Give them ONE deterministic market-state instrument — with receipts — instead.
Rules produce the state (zero LLM in that path); your agents reason over it.

Works with no key (BTCUSDT demo). Set DECKER_API_KEY for any symbol/timeframe.

    python langgraph_decker_tool.py
"""
import json
import os
import urllib.parse
import urllib.request

DECKER_API = "https://api.decker-ai.com/api/v1"
API_KEY = os.environ.get("DECKER_API_KEY")  # optional


def decker_market_state(symbol: str = "BTCUSDT", timeframe: str = "1h") -> dict:
    """Deterministic market-state read for `symbol` on `timeframe`.

    Returns FSM phase (c_state), direction, ref_price, wait_target,
    invalidation, plain-language compact_lines, verdict_recent (receipts),
    and provenance (trace to the rulebook version). No LLM in this path —
    same input always yields the same output.
    """
    headers = {"Accept": "application/json", "User-Agent": "decker-langgraph/1.0"}
    if API_KEY:
        q = urllib.parse.quote(timeframe)
        url = f"{DECKER_API}/public/signals/{symbol}/latest?timeframe={q}"
        headers["X-API-Key"] = API_KEY
    else:
        url = f"{DECKER_API}/public/demo"  # BTCUSDT only, no auth
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.load(r)


# --- Drop into LangChain / LangGraph -----------------------------------------
# from langchain_core.tools import tool
#
# @tool
# def market_state(symbol: str, timeframe: str = "1h") -> str:
#     """Deterministic market-state read (FSM phase, entry/target/stop-style
#     coordinates, and hit/miss receipts). Call this before your analysts
#     argue about direction — it is the ground truth they reason over."""
#     return json.dumps(decker_market_state(symbol, timeframe), ensure_ascii=False)
#
# # then bind it: llm.bind_tools([market_state])  /  ToolNode([market_state])

# --- Drop into AutoGen --------------------------------------------------------
# from autogen import register_function
# register_function(
#     decker_market_state,
#     caller=analyst_agent, executor=user_proxy,
#     name="decker_market_state",
#     description="Deterministic market-state read with receipts (no LLM in path).",
# )

if __name__ == "__main__":
    state = decker_market_state()
    print(json.dumps(
        {k: state[k] for k in ("name", "timeframe", "c_state", "direction",
                               "ref_price", "wait_target", "invalidation")
         if k in state},
        indent=2, ensure_ascii=False,
    ))
    print("\ncompact_lines:")
    for line in state.get("compact_lines", []):
        print(" ", line)

# For information only. Not investment advice. Decker does not custody funds.
