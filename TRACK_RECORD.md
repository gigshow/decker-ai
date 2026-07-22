# Track record — the engine scores its own views, daily

Most signal products show you the wins. This file is the opposite: a
GitHub Action appends **one row per resolved day**, straight from the live
public API — no cherry-picking, no editing. Each row = that morning's views,
scored on the record after their window closed. The repo itself is the
receipt that the engine runs, deterministically, in the open. Corrections
stay in git history.

> Direction scoring (current): `correct` = the shown direction was realized at the view's horizon close · `wrong` = price went the other way · `flat` = barely moved (within the deadband) · `pending` = horizon bar not closed yet · `unscorable` = no candle to score. Rows before 2026-07-15 use the legacy coordinate vocabulary (`hit`/`miss`/`invalidated`) — kept as-is, corrections stay in git history. Full daily briefing + per-view tracking: [decker-ai.com/briefing](https://decker-ai.com/briefing).

| Date (UTC) | Scope | Scorecard (correct · wrong · flat) | Sample views (outcome) |
|------------|-------|--------------------------------------|------------------------|
| 2026-07-22 | 14 views | wrong 1 · flat 1 | BTCUSDT + → barely moved, ETHUSDT - → direction wrong |
| 2026-07-21 | 14 views | correct 6 | BNBUSDT + → direction correct, BTCUSDT + → direction correct, DOGEUSDT + → direction correct |
| 2026-07-20 | 14 views | correct 5 · wrong 5 · flat 3 | BNBUSDT + → direction correct, BTCUSDT + → direction wrong, DOGEUSDT + → direction wrong |
| 2026-07-19 | 14 views | correct 6 · wrong 3 · flat 5 | BNBUSDT + → barely moved, BTCUSDT - → direction wrong, DOGEUSDT + → direction wrong |
| 2026-07-18 | 14 views | correct 4 · wrong 4 · flat 6 | BNBUSDT + → direction wrong, BTCUSDT - → direction wrong, DOGEUSDT + → barely moved |
| 2026-07-17 | 13 views | correct 8 · wrong 3 | BNBUSDT - → direction correct, BTCUSDT - → direction correct, DOGEUSDT - → direction correct |
| 2026-07-16 | 14 views | correct 3 · wrong 7 · flat 4 | BNBUSDT - → direction wrong, BTCUSDT + → direction wrong, DOGEUSDT + → direction wrong |
| 2026-07-15 | 13 views | correct 6 · wrong 3 · flat 4 | BNBUSDT + → barely moved, BTCUSDT + → direction correct, DOGEUSDT + → direction wrong |
| 2026-07-14 | 14 views | invalidated 14 | BNBUSDT + → view changed (legacy), BTCUSDT - → view changed (legacy), DOGEUSDT + → view changed (legacy) |
| 2026-07-13 | 12 views | hit 1 · miss 4 · invalidated 7 | BNBUSDT + → view changed (legacy), BTCUSDT + → view changed (legacy), DOGEUSDT + → view changed (legacy) |
| 2026-07-12 | 14 views | hit 2 · miss 5 · invalidated 7 | BNBUSDT + → view changed (legacy), BTCUSDT + → held / no target (legacy), DOGEUSDT + → view changed (legacy) |
| 2026-07-11 | 14 views | miss 6 · invalidated 8 | BNBUSDT + → held / no target, BTCUSDT + → held / no target, DOGEUSDT - → view changed |
| 2026-07-10 | 14 views | miss 6 · invalidated 8 | BNBUSDT + → view changed, BTCUSDT - → view changed, DOGEUSDT + → view changed |
| 2026-07-09 | 8 views | hit 1 · miss 4 · invalidated 3 | BNBUSDT - → view changed, BTCUSDT - → view changed, DOGEUSDT - → target hit |
| 2026-07-08 | 7 views | hit 3 · invalidated 4 | BTCUSDT + → view changed, DOGEUSDT - → target hit, ETHUSDT + → view changed |
| 2026-07-07 | 7 views | miss 3 · invalidated 4 | BNBUSDT + → held / no target, BTCUSDT + → held / no target, DOGEUSDT - → view changed |
| 2026-07-06 | 3 views | miss 1 · invalidated 2 | BTCUSDT - → view changed, DOGEUSDT - → view changed, ETHUSDT + → held / no target |
| 2026-07-05 | 2 views | hit 1 · invalidated 1 | BTCUSDT short → target hit, ETHUSDT long → view changed |

## Weekly digest — same views, grouped by symbol (last 7 resolved days)

| Symbol | correct | wrong | flat | legacy | latest outcome |
|--------|---------|-------|------|--------|----------------|
| BNBUSDT | 3 | 2 | 2 | 0 | + → direction correct |
| BTCUSDT | 3 | 4 | 1 | 0 | + → barely moved |
| DOGEUSDT | 2 | 4 | 1 | 0 | + → direction correct |
| ETHUSDT | 4 | 3 | 1 | 0 | - → direction wrong |
| SOLUSDT | 5 | 1 | 1 | 0 | + → direction correct |
| XRPUSDT | 4 | 3 | 0 | 0 | + → direction correct |
| XYZ_BRENTOILUSD | 2 | 1 | 1 | 0 | - → direction correct |
| XYZ_CLUSD | 3 | 1 | 2 | 0 | + → direction wrong |
| XYZ_GOLDUSD | 1 | 2 | 3 | 0 | + → barely moved |
| XYZ_KR200USD | 2 | 1 | 2 | 0 | + → barely moved |
| XYZ_NVDAUSD | 4 | 0 | 2 | 0 | + → direction correct |
| XYZ_SILVERUSD | 1 | 3 | 1 | 0 | + → direction wrong |
| XYZ_SP500USD | 3 | 0 | 2 | 0 | - → direction correct |
| XYZ_TSLAUSD | 1 | 1 | 4 | 0 | - → barely moved |

_For information only. Not investment advice._
