# Distributed Rate Limiter — Interview Pack

This pack is designed for a 45–60 min senior backend live-coding exercise.
It includes:
- A minimal FastAPI service.
- In-memory **Sliding Window** limiter.
- **Redis-backed** sliding-window limiter via atomic Lua.
- Docker Compose to run Redis.
- Pytest tests you can extend during the interview.
- An evaluation rubric.

## Quick Start

### 1) Local (no Redis) — in‑memory limiter
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Try it:
curl -i 'http://127.0.0.1:8000/ping?user_id=alice'
```

### 2) With Redis (distributed)
```bash
docker compose up -d
export RATE_LIMIT_BACKEND=redis
export REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload
```

Hit the endpoint multiple times to observe 429 responses after the limit is reached.

### 3) Run tests
```bash
pytest -q
```

## Exercise Prompt (give to candidate)

**Goal:** Implement a per-user rate limiter allowing **N requests per T seconds**, enforceable across multiple backend instances.

**Phase A (code):**
1) Implement/extend the in-memory sliding-window limiter: `allow(user_id: str) -> bool` with proper trims & edge handling.
2) Add/extend tests (around window edges, bursts, parallel calls).

**Phase B (distributed):**
3) Adapt limiter for multi-instance deployment using Redis. Ensure **atomicity** and **bounded memory**. Avoid clock skew issues.
4) Expose `/ping` endpoint that uses the limiter; return 200 if allowed, 429 otherwise. Optional: include `Retry-After`.

**Stretch goals (if time):**
- Add `Retry-After` (seconds to next allowed).
- Add global limit (all users), or per-endpoint limits.
- Observability counters (allowed/denied).

## Evaluation Rubric (for interviewer)

- **Correctness**: ≤ N requests in any sliding T-second window. Boundary handling near rollover.
- **Concurrency**: Thread-safe local impl; atomic Redis ops (Lua or equivalent).
- **Performance**: Amortized O(1)/O(log n); bounded memory via TTL/trim.
- **Resilience**: Behavior when Redis is unavailable; clock skew mitigation; key TTLs.
- **Code quality**: Readability, tests, small functions, naming; comments where needed.
- **Communication**: Clear tradeoffs (sliding vs token bucket; fairness; cost).

## Files

- `app/limiter_memory.py` — In-memory sliding window.
- `app/limiter_redis.py` — Redis Lua-based limiter.
- `app/main.py` — FastAPI app wiring both limiters.
- `app/config.py` — Settings (env-driven).
- `docker-compose.yml` — Redis service.
- `requirements.txt` — Python deps.
- `tests/test_limiter.py` — Basic tests.
- `tests/test_api.py` — API-level tests (FastAPI).

Good luck!
