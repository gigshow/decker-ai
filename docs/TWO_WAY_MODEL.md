# Decker 접근 방법 — 한 페이지

**목적**: 같은 Decker 엔진(시그널·상태·룰북)을 **어떤 방법으로 쓸 수 있는지** 사실 그대로 정리한다. 순위·전략이 아니라 **제공 기능 목록**이다. 상태(✅ 실증/⚠ 제약)는 [AGENT_ENDPOINT_VERIFICATION.md](./AGENT_ENDPOINT_VERIFICATION.md)(2026-07-08 실호출) 기준.

**갱신**: 2026-07-08

---

## 같은 엔진, 여러 입구

```
        ┌─────────────────────────────────────┐
        │  Decker 엔진 · State · RULES · API   │
        └─────────────────┬───────────────────┘
   ┌──────────────┬───────┴───────┬──────────────┐
   ▼              ▼               ▼              ▼
 텔레그램 봇     MCP 서버        OpenClaw 스킬    공개 API / turnkey
 @deckerclawbot  (내 에이전트)    (내 OpenClaw)   (직접 / 자가배포)
```

## 접근 방법 표

| 방법 | 무엇을 하나 | 읽기 | 주문 | 진입 |
|------|-------------|:----:|:----:|------|
| **텔레그램 봇** (@deckerclawbot) | Decker 호스팅 자체 에이전트 — 자연어로 시그널·포지션·주문 | ✅ | ✅ (실주문 검증) | 가입 → 설정 → 텔레그램 연동 → [@deckerclawbot](https://t.me/deckerclawbot) |
| **MCP 서버** | 내 Claude/에이전트(Desktop·Cursor)를 Decker에 연결 (7 tools) | ✅ | — | [decker-ai.com/mcp](https://decker-ai.com/mcp) · 설정 → API 키 |
| **OpenClaw 스킬** | 내 OpenClaw 에이전트에 스킬 추가 (web_fetch) | ✅ | ⚠ Slack 연동자만 | [openclaw_skills/README.md](./openclaw_skills/README.md) |
| **공개 REST API** | 백엔드 직접 (X-API-Key / 무인증 read) | ✅ | — | [DEVELOPER_API_GUIDE.md](./DEVELOPER_API_GUIDE.md) · [api.decker-ai.com/docs](https://api.decker-ai.com/docs) |
| **turnkey** | OpenClaw 없이 내 텔레그램 봇 자가 배포 | ✅ | (설정에 따라) | [turnkey/README.md](../turnkey/README.md) |

> **읽기(시그널·상태·시장)는 모든 방법에서 제공**. **주문**은 텔레그램 봇(@deckerclawbot)에서 실주문까지 지원되며, OpenClaw 스킬은 Slack 연동된 사용자에 한한다(셀프 연동 페이지는 현재 미제공). 신규 사용자 주문은 @deckerclawbot 를 안내.

---

## 누구에게 무엇인가

| 대상 | 방법 |
|------|------|
| 바로 써보기 (비개발자) | **텔레그램 봇** — [@deckerclawbot](https://t.me/deckerclawbot) |
| 내 에이전트(Claude 등)에 붙이기 | **MCP** — [decker-ai.com/mcp](https://decker-ai.com/mcp) |
| 내 OpenClaw 에이전트 | **OpenClaw 스킬** — [openclaw_skills/README.md](./openclaw_skills/README.md) |
| 백엔드만 붙이기 | **공개 API** — [api-guide.md](./api-guide.md) |
| 내 봇 자가 배포 | **turnkey** — [turnkey/README.md](../turnkey/README.md) |

---

## 혼동 방지

| 오해 | 실제 |
|------|------|
| "DeckerClaw = 전부 OpenClaw 기반" | **아님.** 텔레그램 봇(@deckerclawbot)은 Decker 자체 에이전트고, 내 에이전트 연결은 MCP·OpenClaw 두 방법이 있다. |
| "OpenClaw `decker-link` 페이지에서 연동" | **구 경로 폐지(404).** 현재 연동 = 로그인 → 설정 → 텔레그램 / API 키. |
| "주문은 아무 방법이나 된다" | 주문은 **@deckerclawbot** 에서(실주문 검증). OpenClaw 스킬 주문은 Slack 연동자만. |

---

## 더 읽기

| 문서 | 용도 |
|------|------|
| [AGENT_ENDPOINT_VERIFICATION.md](./AGENT_ENDPOINT_VERIFICATION.md) | 각 방법 실호출 검증 결과 |
| [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) | 스킬·명령 짧은 인덱스 |
| [ONBOARDING_PUBLIC.md](./ONBOARDING_PUBLIC.md) | 페르소나별 온보딩 |
| [architecture.md](./architecture.md) | 에이전트 레이어 다이어그램 |
