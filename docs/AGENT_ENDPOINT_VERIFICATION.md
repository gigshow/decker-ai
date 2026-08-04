# 에이전트·엔드포인트 실증 검증

**목적**: Decker 공개 API·MCP·OpenClaw 스킬이 **문서대로 실제 작동하는지 직접 호출로 검증**한 기록. 스킬·가이드가 약속하는 엔드포인트의 실측 결과 단일 출처.

**최종 검증**: 2026-07-08 (prod `api.decker-ai.com`, 실 호출)

**방법**: 각 엔드포인트를 실제 호출(curl / 실 MCP 클라이언트)해 HTTP 상태 + 응답 필드 확인. 인증 항목은 read-only 공개 키(`permissions=read:signals,read:market_data`)로 검증.

---

## 1. 공개 REST (무인증) — "Try It Now"

| 엔드포인트 | 결과 |
|-----------|------|
| `GET /api/v1/public/health` | ✅ 200 |
| `GET /api/v1/public/demo` | ✅ 200 (`layer·symbol·lines·axis`) |
| `GET /api/v1/public/stats` | ✅ 200 (`engine·total_evaluations·symbols`) |

## 2. 시그널·시장 데이터 (무인증 REST — OpenClaw `web_fetch` read 경로)

| 엔드포인트 | 결과 |
|-----------|------|
| `GET /api/v1/judgment/coverage` | ✅ 200 |
| `GET /api/v1/judgment/signals/public?symbol=BTCUSDT&timeframe=1h` | ✅ 200 |
| `GET /api/v1/market/prices?symbols=BTCUSDT,ETHUSDT` | ✅ 200 |
| `GET /api/v1/market-analysis/market-condition/BTCUSDT` | ✅ 200 |
| `GET /api/v1/judgment/compare?symbols=…&timeframe=1h` | ✅ 200 |
| `GET /api/v1/judgment/market-status?interval=24h` | ✅ 200 |
| `GET /api/v1/liquidations/summary` | ✅ 200 |

## 3. 개발자 공개 API (`X-API-Key`)

| 엔드포인트 | 결과 |
|-----------|------|
| `POST /api/v1/public/auth/verify` | ✅ 200 (`valid·tier·permissions`) |
| `GET /api/v1/public/signals/{symbol}/latest?timeframe=1h` | ✅ 200 (`direction·entry_price·target_price·stop_price·progress_pct·action_gate`) |
| `GET /api/v1/public/signals/{symbol}/narrative?timeframe=4h` | ✅ 200 (`narrative·axis`) |
| (참고) 키 없이 호출 | ⚠ 422 Validation — 깨끗한 401/403 대신. 백엔드 정정 백로그 |

## 4. MCP 서버 (Streamable HTTP, stateless + JSON-RPC 2.0)

> ⚠ **2026-08-04 갱신**: 아래 §4 원문(2026-07-08 검증)은 구 SSE 서버(`/mcp/sse`+`/mcp/messages`, in-memory 세션) 기준 — 그날 이후 `041ac6c`(2026-07-10)로 stateless `/api/v1/mcp` 단일 엔드포인트로 컷오버됨. 등록 URL을 안 바꾼 기존 클라이언트는 "session not found"(404)를 계속 겪는다 — 아래는 이번 실사용자 재검증 결과, §4 나머지 항목(다른 섹션)은 미재검증.

| 항목 | 결과 |
|------|------|
| `GET /api/v1/mcp/health` | ✅ 200 (`protocol 2024-11-05`) |
| `POST /api/v1/mcp` `tools/list` | ✅ 200, 9 tools (실측 2026-08-04) |
| 구 `/api/v1/mcp/sse` (신규 등록) | 🔴 405 Method Not Allowed — 완전 폐기됨 |

- **9 tools (실측)**: `get_signals·get_assembly·get_reading·get_view·get_market_state·get_state_timeline·get_user_skills·set_skill_overlay·validate_intent` — 이전 메모("get_assembly·validate_intent 미기재")는 부정확했음: `validate_intent`는 이미 DEVELOPER_README 표에 있었고, 실누락은 `get_assembly` 1건뿐. DEVELOPER_README "8 tools"→"9 tools" 헤더+행 추가, README 가격표 "7 tools"→"9 tools" 모두 수정 완료(2026-08-04).
- **진입**: [decker-ai.com/mcp](https://decker-ai.com/mcp). 엔드포인트는 **stateless** — 세션 유지 불필요, 매 요청 독립. 클라이언트 등록 URL 변경은 **새 세션/앱 재시작 후에만 적용** — 실행 중인 세션은 재시작 전까지 구 커넥션 유지.

## 5. OpenClaw 스킬 — 능력별 상태

| 능력 | 상태 |
|------|------|
| **READ** (시그널·상태·시장) | ✅ 위 §1~3 으로 **작동 — 연결 불필요**(공개 REST / `X-API-Key`) |
| **ORDER/에이전트** (Slack) | ⚠ API 는 mounted(`X-OpenClaw-Secret` + `slack_channel_user_links`), 그러나 **셀프연결 페이지(`decker-link`) 부재** → 셀프서브 주문 미제공. 주문은 Decker 자체 텔레그램/웹으로 |

## 알려진 갭 (문서에 반영해야 할 실상)

- `decker-ai.com/decker-link`·`/decker-link-telegram` = **404** (구 셀프연결 페이지 폐지). 스킬의 주문·연동 안내는 이 상태를 반영해야 한다(READ 는 연결 없이 됨).
- 개발자 API `X-API-Key` 누락 시 **422** → 깨끗한 401/403 으로 정정(백엔드).

---

*이 문서는 실제 호출 결과다. 엔드포인트·스킬 변경 시 재검증하고 날짜·결과를 갱신한다. 요약 인덱스: [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md).*
