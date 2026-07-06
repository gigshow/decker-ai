# Performance — a living ledger, not a marketing number

> **We do not advertise returns or win rates.** An earlier version of this page carried
> backtest profit figures; we removed them deliberately. Decker sells *state reading
> accuracy*, not profit promises — and reading accuracy is something you can audit live.

## What we publish instead

Every engine view is **stamped per bar and scored in public**:

| Surface | What it shows |
|---|---|
| **Daily briefing** (Telegram · [decker-ai.com/briefing](https://decker-ai.com/briefing)) | Morning: the engine's view per symbol (baseline, what winning/losing looks like). **Evening: the same view scored against what actually happened** — hit, miss, invalidated. Misses are printed, not hidden. |
| **Signal lifecycle** | Every signal carries entry / stop / target + `progress_pct`. When the invalidation line is hit, the signal is stamped `invalidated` on the chart and in the API — permanently. |
| **/review** | Your own trades measured against the engine's signals. |
| **`trace_id`** | Every output traces to a bar-stamped ledger row — same input, same output, reproducible. |

## Why this framing

- A signal service that only shows its winners is unfalsifiable. Ours stamps every view,
  every bar, in advance — that is the product.
- Accuracy statement: **state accuracy — yes · profit guarantee — no.** Markets carry risk;
  what we provide is a structural reading you can verify, then decide with.

**See the live numbers yourself**: [decker-ai.com/briefing](https://decker-ai.com/briefing) ·
[decker-ai.com/today](https://decker-ai.com/today) · Telegram [@deckerclawbot](https://t.me/deckerclawbot)
