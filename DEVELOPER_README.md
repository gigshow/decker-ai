<div align="center">

<img src="assets/decker_claw_owl_v1.svg" width="72" alt="DeckerClaw" />

# Decker AI — Developer Guide

Build with Decker: REST API · MCP server · Python SDK · OpenClaw skill · [multi-agent crews](docs/integrations/multi-agent-frameworks.md).

[Main README](README.md) · [API docs](https://api.decker-ai.com/docs) · [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md)

</div>

---

## Contents

- [API quickstart (3 steps)](#api-quickstart-3-steps)
- [Endpoints](#endpoints)
- [Auth](#auth)
- [Rate limits](#rate-limits)
- [MCP server (Way E) — full guide](#mcp-server-way-e)
- [Multi-agent frameworks (TradingAgents · LangGraph · AutoGen)](docs/integrations/multi-agent-frameworks.md)
- [Python SDK](#python-sdk)
- [OpenClaw skill (Way 2)](#openclaw-skill-way-2)
- [Self-host (Way D)](#self-host-way-d)
- [Supported symbols & timeframes](#supported-symbols--timeframes)
- [FAQ](#faq)

---

## API quickstart (3 steps)

### 1. Get your API key — 30 seconds

**Web (fastest)**: [decker-ai.com](https://decker-ai.com) → sign up → **Settings → API Keys → issue**. The key is shown once — copy it immediately.

**Telegram (alternative)**: [@deckerclawbot](https://t.me/deckerclawbot) → `/start` → `/apikey`.

> **Lost your key?** Issue a new one in Settings → API Keys (old keys can be revoked there), or run `/apikey reset` in the bot.

### 2. First call

```bash
curl "https://api.decker-ai.com/api/v1/public/signals/BTCUSDT/latest?timeframe=1h" \
  -H "X-API-Key: dk_live_xxx"
```

```json
{
  "symbol": "BTCUSDT",
  "timeframe": "1h",
  "direction": "long",
  "entry_price": 94200.0,
  "target_price": 97500.0,
  "stop_loss": 92800.0,
  "progress_pct": 67.3,
  "operation_gate": "GO",
  "generated_at": "2026-04-23T05:00:00Z"
}
```

### 3. Try without auth

```bash
curl https://api.decker-ai.com/api/v1/public/demo
```

Returns a live BTCUSDT 1h signal — no API key needed. Useful for smoke testing.

---

## Endpoints

Full OpenAPI spec: **[api.decker-ai.com/docs](https://api.decker-ai.com/docs)**.

### Public — `X-API-Key` required (except `/health` and `/demo`)

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/public/auth/verify` | Verify API key + get tier |
| `GET`  | `/api/v1/public/health` | Liveness (no auth) |
| `GET`  | `/api/v1/public/demo` | Live demo signal (no auth) |
| `GET`  | `/api/v1/public/signals/{symbol}/latest` | Latest signal (direction, entry, target, stop, progress) |
| `GET`  | `/api/v1/public/signals/{symbol}/narrative` | Rule-based / LLM structural narrative |
| `GET`  | `/api/v1/public/signals/{symbol}/mtf` | MTF consumer signal + Skill Overlay applied |
| `GET`  | `/api/v1/public/state/live` | Engine state (c_state · gate · MTF) |
| `GET`  | `/api/v1/public/state/{symbol}/{tf}` | **Market State v0** — persisted per-bar engine state, read as-is (zero recompute). `state` (label · swing · c_state · gate) + `why` (reason_codes · hold_reason · mtf_verdict) + `provenance` |
| `GET`  | `/api/v1/public/state/{symbol}/{tf}/timeline` | Per-bar state timeline (`since`, `limit` ≤ 500). Bars the engine did not emit are simply absent — honest gaps, no filling |

**Market State v0 coverage** — one schema, three symbol families:

| Family | Symbol format | Timeframes | Refresh | Provenance |
|--------|---------------|------------|---------|------------|
| Crypto (Binance) | `BTCUSDT` | `30m` `1h` `4h` `8h` `1d` | real-time (bar close) | `engine:live_l1` |
| Hyperliquid TradFi (HIP-3) | `XYZ_SP500USD` | same | same | `engine:live_l1:hyperliquid_xyz` |
| KRX Korean stocks | `000270.KRX` | `1d` `1w` | daily 16:30 KST (`1w` Fri 17:00) | `krx:daily` |

KRX is a daily batch, so a large `freshness_sec` is the honest value, not staleness.
| `GET`  | `/api/v1/public/reading/{sym}/{tf}` | AI reading view v0.2 (8 blocks) |

### KRX (Beta — free)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/v1/public/krx/signals` | KOSPI + KOSDAQ batch with 4 actions (ADD/HOLD/REDUCE/EXIT) |
| `GET` | `/api/v1/public/krx/market` | Market macro + signal summary |
| `GET` | `/api/v1/public/krx/transitions` | **Daily checkup** — only tickers whose state/gate actually changed at today's close (noise-zero diff; powers the site strip and the Telegram closing-bell briefing) |

```bash
curl -H "X-API-Key: $KEY" \
  'https://api.decker-ai.com/api/v1/public/krx/signals?gate=GO&market=KOSPI&limit=10'
```

Korean-market context: DART filing recency · KOSPI200 RS · price-limit lock state · foreign net-buy*.
*Foreign / market-cap / fundamentals = KIS Open API integration in Q3–Q4 2026.

KRX details: [`docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md`](docs/krx/KRX_BUSINESS_MODEL_AND_ROADMAP_2026-05-09.md).

### MCP

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/api/v1/mcp/sse` | SSE handshake ([Way E](#mcp-server-way-e)) |
| `POST` | `/api/v1/mcp/messages` | JSON-RPC 2.0 (7 tools) |
| `GET`  | `/api/v1/mcp/health` | MCP server health |

---

## Auth

```
X-API-Key: dk_live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Keys are issued from the web UI (**Settings → API Keys**) or via Telegram `/apikey`. See [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md) for full auth flow, scopes, and rotation.

---

## Rate limits

Every response includes:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 17
X-RateLimit-Reset: 1735689600
```

Exceeded → HTTP `429` with `Retry-After`.

| Tier | Daily limit | MCP | Auto-trade |
|------|-------------|-----|-----------|
| **FREE** | 30 calls / day | read-only (1d cache) | ❌ |
| **PRO** | 10,000 / day | full (7 tools) | virtual + real |
| **ENTERPRISE** | 100,000+ / day · custom | full + per-org skill catalog | + custom integration |

> **Beta (now):** authenticated users get **PRO for free** via `BETA_TIER_OVERRIDE=PRO`. No payment required.

---

## MCP Server (Way E)

Add Decker AI to any [MCP-compatible](https://modelcontextprotocol.io/) AI agent — Claude Desktop, Cursor, Codex, or your own MCP client. Same `X-API-Key`, same Skill Overlay, same rulebook.

> **New here?** The fastest path is the step-by-step page → **[decker-ai.com/mcp](https://decker-ai.com/mcp)** (per-client config for Claude Desktop / Cursor / Codex, copy-paste prompts, troubleshooting). This section is the reference.

### Endpoints (live)

```
GET  https://api.decker-ai.com/api/v1/mcp/sse           (SSE handshake)
POST https://api.decker-ai.com/api/v1/mcp/messages      (JSON-RPC 2.0)
GET  https://api.decker-ai.com/api/v1/mcp/health        (monitoring)
```

Config differs by client — pick yours (or use the guided page: **[decker-ai.com/mcp](https://decker-ai.com/mcp)**).

### Claude Desktop / Codex (via `mcp-remote`, needs Node/npx)

`Settings → Developer → Edit Config` (Claude Desktop) or `~/.codex/config.toml` (Codex). Claude Desktop reaches a remote SSE server through the `mcp-remote` bridge:

```json
{
  "mcpServers": {
    "decker": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.decker-ai.com/api/v1/mcp/sse", "--header", "X-API-Key:${DECKER_API_KEY}"],
      "env": { "DECKER_API_KEY": "dk_live_YOUR_KEY" }
    }
  }
}
```

### Cursor (native remote SSE — no bridge)

`~/.cursor/mcp.json` accepts a URL + headers directly:

```json
{
  "mcpServers": {
    "decker": {
      "url": "https://api.decker-ai.com/api/v1/mcp/sse",
      "headers": { "X-API-Key": "dk_live_YOUR_KEY" }
    }
  }
}
```

Then fully quit and reopen the app — Decker tools appear in the tool picker. Verify the server + tool list with no key: `curl https://api.decker-ai.com/api/v1/mcp/health`.

### 7 tools (auto-applies your active Skill Overlay)

| Tool | Purpose | Key params |
|------|---------|-----------|
| **`decker.get_view`** ★ | **The engine's VIEW — the same composed card the daily briefing sends** (single composer): verdict, plain-language narrative, coordinates (ref/target/invalidation), "at this price, this view", recent self-scoring (receipts). Start here. | `symbol` |
| `decker.get_signals` | Active consumer signals (Skill Overlay applied) | `symbols?` (array), `min_progress?`, `action_gate?` (GO/WATCH/HOLD — rows with no engine gate emit are excluded), `limit?` |
| `decker.get_reading` | AI reading view v0.2 (8 blocks: state · MTF · risk · narrative) | `symbol`, `tf?` (default 4h), `include_tfs?` (comma list) |
| `decker.get_market_state` | **Market State v0** — current engine structural state for a bar (persisted emit, zero recompute). `action_gate` is a transition posture (GO/WATCH/HOLD), not an order command; absent axes are `null` | `symbol`, `timeframe` (30m/1h/4h/8h/1d) |
| `decker.get_state_timeline` | Per-bar state timeline, same schema, ascending by `bar_ts` | `symbol`, `timeframe`, `since?`, `limit?` |
| `decker.get_user_skills` | Catalog of trading skills + active overlay | — |
| `decker.set_skill_overlay` | Switch overlay on the fly | `skill_id` — one of 8: `conservative_v0` \| `standard_v0` \| `aggressive_v0` \| `default_v0` \| `scalp_v0` \| `tight_v0` \| `wide_v0` \| `swing_v0` (full catalog via `get_user_skills`) |

All tool calls inherit the API key's tier (FREE = read-only with cache, PRO = full). Tool responses are JSON-RPC 2.0; errors return standard `{ "error": { "code": ..., "message": ... } }`.

### Smoke test (curl)

```bash
# 1. Handshake (will hang — Ctrl+C after seeing "endpoint")
curl -N -H "X-API-Key: dk_live_xxx" \
  https://api.decker-ai.com/api/v1/mcp/sse

# 2. List tools
curl -X POST https://api.decker-ai.com/api/v1/mcp/messages \
  -H "X-API-Key: dk_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 3. Call a tool
curl -X POST https://api.decker-ai.com/api/v1/mcp/messages \
  -H "X-API-Key: dk_live_xxx" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"decker.get_signals","arguments":{"symbols":["BTCUSDT"]}}}'
```

Full step-by-step guide (per-client config, prompts, troubleshooting): **[decker-ai.com/mcp](https://decker-ai.com/mcp)**.

---

## Python SDK

The SDK is included in this repository at [`sdk/python/`](sdk/python/).

```bash
git clone https://github.com/gigshow/decker-ai.git
pip install -e decker-ai/sdk/python/
```

```python
from decker_client import Client, RateLimitError, AuthError, NotFoundError

with Client(api_key="dk_live_xxx") as client:
    sig = client.signals.get_latest("BTCUSDT", timeframe="1h")
    print(f"{sig.direction} | entry={sig.entry_price} | progress={sig.progress_pct}%")

    narr = client.signals.get_narrative("BTCUSDT", "4h")
    print(narr.text)

    rl = client.last_rate_limit
    print(f"{rl.remaining}/{rl.limit} remaining today")
```

**Error handling:**

```python
try:
    sig = client.signals.get_latest("BTCUSDT")
except AuthError:
    print("Invalid API key — run /apikey reset in Telegram")
except NotFoundError:
    print("No active signal for this symbol/timeframe")
except RateLimitError as e:
    print(f"Rate limited — retry in {e.retry_after}s")
```

> `pip install decker-client` (PyPI) is planned — not yet published. Use the local install above until then.
> Full reference: [sdk/python/README.md](sdk/python/README.md).

---

## OpenClaw skill (Way 2)

Add Decker as a skill to your OpenClaw agent — `web_fetch` against the REST API, with the rulebook applied server-side.

Skill packages live in [`docs/openclaw_skills/`](docs/openclaw_skills/).

---

## Self-host (Way D)

One-click Railway deploy of the API + worker stack lives in [`turnkey/`](turnkey/). Bring your own database; the rulebook ships in `operation_rules/RULES.yaml`.

---

## Supported symbols & timeframes

**Crypto (GA):** `BTCUSDT` · `ETHUSDT` · `SOLUSDT` · `BNBUSDT` · `XRPUSDT` · `DOGEUSDT`
**Timeframes:** `30m`, `1h`, `4h`, `1d`

**KRX (Beta, free):** KOSPI 948 + KOSDAQ 1,822 = **2,770 tickers**. Universe = top 200 by trading value ∪ user watchlist ∪ momentum spike ∪ volume spike. Timeframe `1d` only (1w expanding). Daily evaluation at 16:30 KST.

Symbols / timeframes outside this list return `404`. More symbols expanding.

---

## FAQ

**Where do I get an API key?**
[decker-ai.com](https://decker-ai.com) → **Settings → API Keys**, or Telegram [@deckerclawbot](https://t.me/deckerclawbot) → `/apikey`.

**Why no `pip install decker-client`?**
PyPI publish is planned; not yet shipped. Until then, install from this repo with `pip install -e sdk/python/`.

**Why is `WATCH` a separate gate?**
Most tools collapse the "signal forming but not confirmed" state into either `BUY` (too early) or `nothing` (silent). Decker keeps it explicit so you can monitor without acting.

**Does the LLM ever override the rules path?**
No. The LLM only **explains** the structural state produced by the deterministic engine. The rules path runs at `$0` LLM cost; the explanation layer is opt-in.

**How is auto-trade gated?**
PRO tier + per-symbol skill enabled in your Strategy preset + execution_mode (`paper` vs `live`) set per channel. See [DEVELOPER_API_GUIDE.md](docs/DEVELOPER_API_GUIDE.md) for the full execution-mode contract.

**Can I use Decker for backtesting?**
The same rulebook (`operation_rules/RULES.yaml`) drives backtest and live evaluation. See [docs/signal-performance.md](docs/signal-performance.md) for our internal backtest methodology.

---

## More docs

| | |
|--|--|
| [Developer API Guide](docs/DEVELOPER_API_GUIDE.md) | Full auth · rate limits · SDK · FAQ |
| [Quick Start](docs/quickstart.md) | 3-step per path |
| [API Guide](docs/api-guide.md) | Endpoint reference (long form) |
| [Architecture](docs/architecture.md) | Pipeline, state engine, modules |
| [Model & Algorithm](docs/model.md) | How the signal engine works |
| [Operation Rules](operation_rules/RULES.yaml) | Open YAML rulebook (v2.4.7+) |
| [llms.txt](llms.txt) | LLM / AI agent discovery manifest |

---

> Building with Decker? Issues + PRs welcome at [github.com/gigshow/decker-ai](https://github.com/gigshow/decker-ai/issues).
> For the user-facing intro, see the [main README](README.md).
