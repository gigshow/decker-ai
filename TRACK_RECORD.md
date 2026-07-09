# Track record — the engine scores its own views, daily

Most signal products show you the wins. This file is the opposite: a
GitHub Action appends **one row per resolved day**, straight from the live
public API — no cherry-picking, no editing. Each row = that morning's views,
scored on the record after their window closed. The repo itself is the
receipt that the engine runs, deterministically, in the open.

> `hit` = view reached its target · `miss` = held, target not reached · `invalidated` = view changed (invalidation line touched) · `unscorable` = no candle to score. Full daily briefing + per-view tracking: [decker-ai.com/briefing](https://decker-ai.com/briefing).

| Date (UTC) | Scope | Scorecard (hit · miss · invalidated) | Sample views (outcome) |
|------------|-------|--------------------------------------|------------------------|
| 2026-07-08 | 11 views | hit 5 · miss 1 · invalidated 5 | BNBUSDT + → view changed, BTCUSDT + → view changed, DOGEUSDT - → target hit |
| 2026-07-07 | 11 views | miss 3 · invalidated 4 · unscorable 4 | BNBUSDT + → held / no target, BTCUSDT + → held / no target, DOGEUSDT - → view changed |
| 2026-07-06 | 13 views | miss 2 · invalidated 8 | BNBUSDT + → held / no target, BTCUSDT - → view changed, DOGEUSDT - → view changed |
| 2026-07-05 | 5 views | hit 1 · miss 1 · invalidated 2 · unscorable 1 | BTCUSDT short → target hit, ETHUSDT long → view changed, XYZ_CLUSD + → held / no target |

_For information only. Not investment advice._
