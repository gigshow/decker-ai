# Examples

Runnable, copy-paste starting points. The Python scripts are **pure stdlib — no
dependencies, no signup, no API key** (they hit the public `BTCUSDT` demo, ~10
requests / IP / day). Set `DECKER_API_KEY` for any symbol + timeframe.

| File | What it does |
|------|--------------|
| [`quickstart.py`](quickstart.py) | 60-second smoke test — prints the composed market-state view + receipts (the same card the daily briefing sends). |
| [`langgraph_decker_tool.py`](langgraph_decker_tool.py) | Wrap Decker as one deterministic market-state tool for a LangChain / LangGraph / AutoGen crew (copy-paste `@tool` / `register_function` snippets inside). |
| [`signal_example.md`](signal_example.md) | Annotated example of a signal payload. |
| [`state_response_masked.example.json`](state_response_masked.example.json) | Full state response shape (masked). |
| [`strategy_prompt_example.md`](strategy_prompt_example.md) | Example strategy prompt. |

```bash
python quickstart.py            # no key needed
DECKER_API_KEY=dk_live_xxx python langgraph_decker_tool.py   # any symbol/timeframe
```

Get a free key: **decker-ai.com → Settings → API Keys** (or Telegram `@deckerclawbot` → `/apikey`).

_For information only. Not investment advice._
