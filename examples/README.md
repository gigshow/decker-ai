# Examples

Runnable, copy-paste starting points. The Python scripts are **pure stdlib — no
dependencies, no signup, no API key** for the demo path (they hit the public
`BTCUSDT` demo, ~10 requests / IP / day). Set `DECKER_API_KEY` for any symbol +
timeframe.

Get a free key: **decker-ai.com → Settings → API Keys** (or Telegram `@deckerclawbot` → `/apikey`).

## Python

| File | What it does |
|------|--------------|
| [`quickstart.py`](quickstart.py) | 60-second smoke test — prints the composed market-state view + receipts (the same card the daily briefing sends). No key. |
| [`langgraph_decker_tool.py`](langgraph_decker_tool.py) | Wrap Decker as one deterministic market-state tool for a LangChain / LangGraph / AutoGen crew (copy-paste `@tool` / `register_function` snippets inside). |
| [`get_signal.py`](python/get_signal.py) | Fetch the latest signal for a symbol/timeframe. `python python/get_signal.py BTCUSDT 1h` |
| [`api-client-python.py`](api-client-python.py) | Minimal API client wrapper. `python api-client-python.py BTCUSDT` |
| [`strategy-demo.py`](strategy-demo.py) | Register a signal and read back the strategy. `python strategy-demo.py BTCUSDT 96000 100000 92000` |
| [`strategy_bot.py`](python/strategy_bot.py) | Small end-to-end strategy bot loop. `python python/strategy_bot.py BTCUSDT` |

## curl / shell

| File | What it does |
|------|--------------|
| [`curl/examples.sh`](curl/examples.sh) | Common read endpoints via curl. `./curl/examples.sh BTCUSDT` |
| [`signal-push-strategy.sh`](signal-push-strategy.sh) | Two-step flow: register a signal → get the strategy. `./signal-push-strategy.sh BTCUSDT 96000 100000 92000` |

## Reference payloads

| File | What it is |
|------|------------|
| [`signal_example.md`](signal_example.md) | Annotated example of a signal payload. |
| [`state_response_masked.example.json`](state_response_masked.example.json) | Full state response shape (masked). |
| [`strategy_prompt_example.md`](strategy_prompt_example.md) | Example strategy prompt. |

```bash
python quickstart.py                                          # no key needed
DECKER_API_KEY=dk_live_xxx python langgraph_decker_tool.py    # any symbol/timeframe
DECKER_API_URL=http://localhost:8000 ./curl/examples.sh BTCUSDT   # point at a local server
```

_For information only. Not investment advice._
