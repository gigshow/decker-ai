# Decker 스킬 가이드

**목적**: Decker 를 **에이전트·IDE·API** 로 쓸 때 참조하는 **스킬 목록과 선택 규칙**의 단일 출처. 사용자·개발자·기여자용.

> 이 저장소는 **공개 허브**(문서·샘플·OpenClaw 스킬 패키지)다. 제품 애플리케이션 코드는 별도 비공개 모노레포에서 돈다.

**갱신**: 2026-07-08

---

## 1. 스킬 두 층 (구조)

| 층 | 대상 | 무엇 | 위치 |
|----|------|------|------|
| **A. 에이전트 연동 스킬 (OpenClaw 패키지)** | 사용자 — 자기 에이전트에 붙임 | 시그널·포지션·주문·시세를 자연어로 | `docs/openclaw_skills/` (이 레포) |
| **B. IDE 도메인 스킬 (`decker-*`)** | 기여자 — Decker 위에서 개발 | 시그널·실행 등 도메인 작업 지침 | 메인(비공개) 모노레포 `.cursor/skills/` |

---

## 2. 에이전트 연동 스킬 (OpenClaw) — 이 레포에서 바로 받기

자신의 OpenClaw/Claude 에 추가하면 자연어로 Decker 를 부린다. 추가 방법·흐름은 [openclaw_skills/README.md](./openclaw_skills/README.md), 두 갈래(Telegram 자체 에이전트 vs OpenClaw) 구분은 [TWO_WAY_MODEL.md](./TWO_WAY_MODEL.md).

| 스킬 | 버전 | 용도 | 파일 |
|------|------|------|------|
| `decker` | 2.3.8 | 시그널·포지션·주문·자동주문·뉴스·Slack/Telegram 연동 | [openclaw_skills/decker/SKILL.md](./openclaw_skills/decker/SKILL.md) |
| `decker-hyperliquid` | 1.2.0 | Hyperliquid DEX 거래·시세·펀딩 | [openclaw_skills/decker-hyperliquid/SKILL.md](./openclaw_skills/decker-hyperliquid/SKILL.md) |
| `decker-polymarket` | 1.1.0 | Polymarket 예측시장 주문·마켓 검색 | [openclaw_skills/decker-polymarket/SKILL.md](./openclaw_skills/decker-polymarket/SKILL.md) |
| `decker-developer` | 1.0.0 | Public API 키 발급·인증·엔드포인트·Rate Limit·Python SDK | [openclaw_skills/decker-developer/SKILL.md](./openclaw_skills/decker-developer/SKILL.md) |

각 `SKILL.md` 는 YAML frontmatter(`name`·`description`·`version`) + 트리거 + API 호출 규칙을 담는다.

---

## 3. IDE 도메인 스킬 (기여자)

Decker **위에서 개발**할 때 참조하는 프로젝트 스킬. 본문은 비공개 모노레포의 `.cursor/skills/decker-*/` 에 있고, 여기서는 개념만 둔다.

| 스킬 | 용도 (언제) |
|------|-------------|
| `decker-signal` | 시그널 수집·저장·배포, Signal LLM, `judgment_signals`, 룰북·tier |
| `decker-execution-mode` | 실행 모드(모의/실), `ExecutionRouter`, 채팅 주문 경로 |

각 `SKILL.md` = YAML frontmatter(`name`·`description`) + 한 장 요약 + 문서 맵 + 코드 경로 표.

---

## 4. 전략 (Strategy)

Decker 의 핵심은 **결정론 상태·게이트 위에서 만드는 전략**이다.

| 자원 | 용도 |
|------|------|
| [strategy-dsl.md](./strategy-dsl.md) | YAML 기반 전략 DSL **사양** — 진입 객체·진행도·다중 TF 정렬. ⚠ 현재 API 는 `RULES.yaml` 형식 지원, DSL 파서는 로드맵 |
| [operation_rules/RULES.yaml](../operation_rules/RULES.yaml) | 결정론 게이트·tier 규칙 (룰북) |
| [engine-recipe-and-run.md](./engine-recipe-and-run.md) · [architecture.md](./architecture.md) | 엔진 상태·판정 개념과 데이터 흐름 |
| [risk-management.md](./risk-management.md) | 포지션·리스크 규칙 |

---

## 5. 사용 경로 요약

- **사용자(텔레그램)**: `/help`, `/services`, `/apikey`, 자연어 — 표는 [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md).
- **개발자(Public API)**: 텔레그램 연동 후 `/apikey` → `dk_live_xxx` 수령 → `X-API-Key` 헤더 → `api.decker-ai.com/docs`. 상세 [DEVELOPER_API_GUIDE.md](./DEVELOPER_API_GUIDE.md).
- **에이전트(OpenClaw)**: §2 에서 스킬 추가 → 트리거("시그널 알려줘") → `web_fetch` → Decker API 응답을 자연어로.

---

## 6. 관련 문서

| 문서 | 용도 |
|------|------|
| [AGENT_SKILLS_PUBLIC_SUMMARY.md](./AGENT_SKILLS_PUBLIC_SUMMARY.md) | ClawHub·릴리즈용 짧은 인덱스 |
| [ONBOARDING_PUBLIC.md](./ONBOARDING_PUBLIC.md) | GitHub 방문자·페르소나별 온보딩 |
| [TELEGRAM_AGENT_COMMANDS.md](./TELEGRAM_AGENT_COMMANDS.md) | 텔레그램 `/` 명령·자연어 |
| [roadmap.md](./roadmap.md) | 로드맵 |
| [openclaw_skills/README.md](./openclaw_skills/README.md) | OpenClaw 패키지·배포 경로 |
| [GITHUB_COMMUNITY.md](./GITHUB_COMMUNITY.md) | Discussions·이슈 템플릿·라벨 |

---

*이 문서가 스킬 목록의 단일 출처다. 표를 바꿀 때는 여기를 먼저 갱신하고 `CLAUDE.md`·`AGENT_SKILLS_PUBLIC_SUMMARY.md` 는 링크·요약만 맞춘다.*
