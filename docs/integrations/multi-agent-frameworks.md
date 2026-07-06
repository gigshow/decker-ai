# Decker × Multi-Agent Trading Frameworks

> **TL;DR** — Frameworks like [TradingAgents](https://github.com/TauricResearch/TradingAgents),
> LangGraph crews, and AutoGen teams orchestrate LLM agents that *decide*. Decker is the
> **deterministic market-state instrument** those agents call. One MCP line (or one REST tool)
> gives your whole crew a shared, auditable ground truth — so your technical analyst stops
> re-deriving market structure from raw candles on every run, and your risk manager gets an
> invalidation line it can actually enforce.

## Why an agent crew needs a deterministic instrument

Multi-agent trading frameworks are great at the *decision* layer: debate, synthesis, role
separation. But every LLM-powered "technical analyst" shares the same weakness — it re-reads
raw price data each run and produces a **non-deterministic, non-auditable** reading. Two runs,
two structures. No receipts.

Decker solves exactly that layer, and only that layer:

| | LLM technical-analyst agent | Decker state engine |
|---|---|---|
| Market structure | re-derived per prompt, varies per run | deterministic state machine — same input, same output |
| Invalidation | prose ("if it breaks support…") | a number: `stop` / baseline, stamped per bar |
| Lifecycle | none | `progress_pct` 0–100 (entry → target) |
| Audit trail | chat log | `trace_id` → bar-stamped ledger row |
| Cost per read | LLM call | **$0** (zero-LLM rules path) |

**Division of labor**: your crew keeps the judgment. Decker supplies the instrument readings.

## What your crew gets per role

| Crew role (TradingAgents-style) | What Decker feeds it |
|---|---|
| **Technical analyst** | **`get_view`** — the interpreted card (verdict · narrative · coordinates · "at this price, this view") straight from the same composer our daily briefing uses; drop to `get_market_state` for raw state-machine fields (phase, gate, MTF) |
| **Risk manager** | hard invalidation line (`stop`), baseline price, `progress_pct` (a 25%-progress signal ≠ an 80% one), per-bar invalidation stamps |
| **Trader** | `entry / target / stop` triplet + gate — actionable coordinates, not prose |
| **Portfolio manager** | one grammar across **crypto (24/7) + Hyperliquid TradFi synthetics (S&P500, gold, oil, NVDA…) + Korean equities (KOSPI/KOSDAQ)** — cross-market state comparison for free |
| **Fundamental / news / sentiment analysts** | keep your own — Decker deliberately does *not* do news or sentiment. Clean separation, no overlap |

## What you can't cheaply rebuild (the moat, stated plainly)

1. **A state engine that never sleeps.** Every bar, every symbol, three markets, one grammar —
   already computed before your agent asks. Your crew queries state; it doesn't run infra.
2. **Receipts.** Every output traces to a bar-stamped ledger row (`trace_id`). When your agent
   crew is asked *"why did you enter?"*, it can cite an auditable, reproducible reading.
3. **A self-scoring track record.** Decker publishes its own view every morning and **scores it
   in public every evening — misses included** ([daily briefing](https://decker-ai.com/briefing)).
   An agent stack built on a tool that stamps its wrong calls inherits that accountability.
4. **A live product, not a research repo.** The same API your agents call powers a running
   service (web · Telegram · MCP) used daily. Endpoints are production-monitored, not demo-ware.

## Wire it in

**MCP (Claude / Cursor / any MCP host) — one config block:**

```json
{
  "mcpServers": {
    "decker-ai": {
      "url": "https://api.decker-ai.com/api/v1/mcp/sse",
      "headers": { "X-API-Key": "dk_live_xxx" }
    }
  }
}
```

**REST tool for LangGraph / AutoGen / custom crews — one function:**

```python
import requests

def get_engine_view(symbol: str) -> dict:
    """The engine's composed VIEW (same card the daily briefing sends): verdict,
    narrative lines, ref/target/invalidation coordinates, recent self-scoring."""
    r = requests.get(
        f"https://api.decker-ai.com/api/v1/public/view/{symbol}",
        headers={"X-API-Key": "dk_live_xxx"},  # decker-ai.com → Settings → API Keys
        timeout=10,
    )
    r.raise_for_status()
    return r.json()  # {layer: STATE_VIEW, lines[], ref_price, wait_target, invalidation, verdict_recent[], provenance}
```

Register it as a tool for your analyst/risk nodes and cite the response (including its
timestamps) in your crew's decision log — that's the receipts pattern.

No key yet? Smoke-test without auth first: `curl https://api.decker-ai.com/api/v1/public/demo`

## Co-building

We're actively looking for multi-agent framework builders to co-work with — adapters,
example crews, benchmark harnesses. Open an issue or start a discussion in this repo,
or reach us via [decker-ai.com](https://decker-ai.com). FREE tier (30 calls/day) is enough
to wire a crew; during open beta all signed-up users get PRO free.

*Accuracy statement: Decker provides state readings, not financial advice. State accuracy —
yes; profit guarantees — no. See [signal-performance.md](../signal-performance.md).*
