# decker-client

Official Python SDK for the [Decker](https://decker-ai.com) crypto signal & narrative engine.

## Install

```bash
pip install decker-client
```

> PyPI 미등록 시 로컬 설치:
> ```bash
> pip install ./sdk/python
> ```

---

## API 키 발급

`https://app.decker-ai.com/settings/apikey` 에서 발급  
또는 Telegram 봇 `/apikey` 명령으로 발급

---

## Quickstart

```python
from decker_client import Client

client = Client(api_key="dk_live_xxx")
```

---

## 주요 사용 패턴

### 1. 지금 진입해도 되나? — 엔진 상태 확인

```python
state = client.state.get_live("BTCUSDT", tf="4h")

print(state.action_gate)    # "GO" | "WATCH" | "HOLD"
print(state.key_direction)  # "+" (롱) | "-" (숏)
print(state.c_state)        # "B_FORMING" | "A_FORMING" | "BREAK_PLUS" | ...

# MTF(멀티 타임프레임) 상태
for tf, snap in state.mtf.items():
    print(f"{tf}: gate={snap.action_gate}, dir={snap.key_direction}")
```

### 2. 구체적 진입가·목표가·손절가 — 소비자 시그널

```python
sig = client.signals.get_consumer("BTCUSDT")

print(sig.entry_price)         # 진입가
print(sig.target_t1)           # 목표가 T1
print(sig.stop_price)          # 손절가
print(sig.risk_reward_ratio)   # R:R 비율
print(sig.mtf_verdict)         # "ALIGNED" | "NEUTRAL" | "MIXED" | "CONFLICT"
print(sig.action_gate)         # "GO" | "WATCH" | "HOLD"

# 내 스킬 overlay 결과 (스킬 설정 시)
print(sig.overlay_filter_pass)  # True / False / None
print(sig.overlay_skill_id)     # "conservative_v0" | "standard_v0" | ...
```

### 3. AI 판독 — 지금 시장이 뭐라고 하나

```python
reading = client.reading.explain("BTCUSDT", "4h")

print(reading.narrative)          # 자연어 시장 설명
print(reading.stance)             # "LONG_BIAS" | "SHORT_BIAS" | "NEUTRAL"
print(reading.preferred_direction) # "+" | "-"
print(reading.mtf_verdict)         # "ALIGNED" | "CONFLICT" | ...
```

### 4. 전체 흐름 — 에이전트 통합 예시

```python
from decker_client import Client, RateLimitError

with Client(api_key="dk_live_xxx") as client:
    # Step 1: 엔진 게이트 확인
    state = client.state.get_live("BTCUSDT", tf="4h")
    if state.action_gate != "GO":
        print(f"대기 중 — gate={state.action_gate}")
    else:
        # Step 2: 진입 정보
        sig = client.signals.get_consumer("BTCUSDT")
        if sig.overlay_filter_pass is False:
            print("내 스킬 조건 미달 — 스킵")
        else:
            # Step 3: AI 판독
            reading = client.reading.explain("BTCUSDT", "4h")
            print(f"[{state.key_direction}] {reading.stance}")
            print(f"진입: {sig.entry_price} / 목표: {sig.target_t1} / 손절: {sig.stop_price}")
            print(reading.narrative)
```

### 5. 기존 메서드 — narrative, latest

```python
# 자연어 요약
narr = client.signals.get_narrative("BTCUSDT", "1h")
print(narr.text)

# 최신 시그널 (단순)
latest = client.signals.get_latest("BTCUSDT")
print(latest.direction, latest.entry_price)
```

---

## Rate Limits

| Tier    | 일일 한도 |
|---------|----------|
| FREE    | 100 req  |
| PRO     | 10,000 req |
| ENTERPRISE | 100,000 req |

```python
from decker_client import RateLimitError

try:
    sig = client.signals.get_consumer("BTCUSDT")
except RateLimitError as e:
    print(f"한도 초과 — {e.retry_after}초 후 재시도")

# 매 요청 후 잔여 확인
rl = client.last_rate_limit
print(f"오늘 {rl.remaining}/{rl.limit} 남음")
```

---

## 에러 처리

| 예외 | HTTP | 의미 |
|------|------|------|
| `AuthError` | 401 | API 키 없음 또는 무효 |
| `PermissionError` | 403 | 권한 없음 |
| `NotFoundError` | 404 | 심볼 없음 |
| `RateLimitError` | 429 | 일일 한도 초과 |
| `APIError` | 5xx | 서버 오류 |

---

## 전체 API 레퍼런스

OpenAPI 스펙: [api.decker-ai.com/docs](https://api.decker-ai.com/docs)

---

## License

MIT
