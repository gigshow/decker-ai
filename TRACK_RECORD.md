# Track record — the engine scores its own views, daily

Most signal products show you the wins. This file is the opposite: a
GitHub Action appends **one row per resolved day**, straight from the live
public API — no cherry-picking, no editing. Each row = that morning's views,
scored on the record after their window closed. The repo itself is the
receipt that the engine runs, deterministically, in the open. Corrections
stay in git history.

> `hit` = view reached its target · `miss` = held, target not reached · `invalidated` = view changed (invalidation line touched) · `unscorable` = no candle to score. Full daily briefing + per-view tracking: [decker-ai.com/briefing](https://decker-ai.com/briefing).

| Date (UTC) | Scope | Scorecard (hit · miss · invalidated) | Sample views (outcome) |
|------------|-------|--------------------------------------|------------------------|
| 2026-07-18 | 14 views | wrong 4 · flat 6 · correct 4 | BNBUSDT + → wrong, BTCUSDT - → wrong, DOGEUSDT + → flat |
| 2026-07-17 | 13 views | correct 8 · wrong 3 | BNBUSDT - → correct, BTCUSDT - → correct, DOGEUSDT - → correct |
| 2026-07-16 | 14 views | wrong 7 · correct 3 · flat 4 | BNBUSDT - → wrong, BTCUSDT + → wrong, DOGEUSDT + → wrong |
| 2026-07-15 | 13 views | flat 4 · correct 6 · wrong 3 | BNBUSDT + → flat, BTCUSDT + → correct, DOGEUSDT + → wrong |
| 2026-07-14 | 14 views | invalidated 14 | BNBUSDT + → view changed, BTCUSDT - → view changed, DOGEUSDT + → view changed |
| 2026-07-13 | 12 views | hit 1 · miss 4 · invalidated 7 | BNBUSDT + → view changed, BTCUSDT + → view changed, DOGEUSDT + → view changed |
| 2026-07-12 | 14 views | hit 2 · miss 5 · invalidated 7 | BNBUSDT + → view changed, BTCUSDT + → held / no target, DOGEUSDT + → view changed |
| 2026-07-11 | 14 views | miss 6 · invalidated 8 | BNBUSDT + → held / no target, BTCUSDT + → held / no target, DOGEUSDT - → view changed |
| 2026-07-10 | 14 views | miss 6 · invalidated 8 | BNBUSDT + → view changed, BTCUSDT - → view changed, DOGEUSDT + → view changed |
| 2026-07-09 | 8 views | hit 1 · miss 4 · invalidated 3 | BNBUSDT - → view changed, BTCUSDT - → view changed, DOGEUSDT - → target hit |
| 2026-07-08 | 7 views | hit 3 · invalidated 4 | BTCUSDT + → view changed, DOGEUSDT - → target hit, ETHUSDT + → view changed |
| 2026-07-07 | 7 views | miss 3 · invalidated 4 | BNBUSDT + → held / no target, BTCUSDT + → held / no target, DOGEUSDT - → view changed |
| 2026-07-06 | 3 views | miss 1 · invalidated 2 | BTCUSDT - → view changed, DOGEUSDT - → view changed, ETHUSDT + → held / no target |
| 2026-07-05 | 2 views | hit 1 · invalidated 1 | BTCUSDT short → target hit, ETHUSDT long → view changed |

## Weekly digest — same views, grouped by symbol (last 7 resolved days)

| Symbol | hit | miss | invalidated | latest outcome |
|--------|-----|------|-------------|----------------|
| BNBUSDT | 0 | 1 | 3 | + → wrong |
| BTCUSDT | 0 | 2 | 2 | - → wrong |
| DOGEUSDT | 0 | 0 | 4 | + → flat |
| ETHUSDT | 0 | 3 | 1 | - → correct |
| SOLUSDT | 1 | 0 | 3 | - → flat |
| XRPUSDT | 0 | 0 | 4 | - → wrong |
| XYZ_BRENTOILUSD | 1 | 1 | 1 | + → correct |
| XYZ_CLUSD | 0 | 2 | 2 | + → correct |
| XYZ_GOLDUSD | 0 | 1 | 3 | + → flat |
| XYZ_KR200USD | 1 | 0 | 3 | + → flat |
| XYZ_NVDAUSD | 0 | 2 | 2 | + → flat |
| XYZ_SILVERUSD | 0 | 1 | 2 | + → wrong |
| XYZ_SP500USD | 0 | 1 | 3 | - → correct |
| XYZ_TSLAUSD | 0 | 1 | 3 | - → flat |

_For information only. Not investment advice._
