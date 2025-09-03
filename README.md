# Distributed Rate Limiter

This project includes:
- A minimal FastAPI service
- In-memory **Sliding Window** limiter
- **Redis-backed** sliding-window limiter
- Docker Compose to run Redis
- Pytest tests

## Quick Start

```bash
uv sync
make dev
# Try it:
curl -i 'http://127.0.0.1:8000/ping?user_id=alice'
```


Hit the endpoint multiple times to observe 429 responses after the limit is reached.

### Run tests
```bash
make test
```

## Exercise

**Goal:** Implement a per-user rate limiter allowing **N requests per T seconds**, enforceable across multiple backend instances.

**Phase A:**
1) Implement/extend the in-memory sliding-window limiter: `allow(user_id: str) -> bool` with proper trims & edge handling.
2) Add/extend tests (around window edges, bursts, parallel calls).

**Phase B:**
1) Adapt limiter for multi-instance deployment using Redis. Ensure **atomicity** and **bounded memory**. Avoid clock skew issues.
2) Expose `/ping` endpoint that uses the limiter; return 200 if allowed, 429 otherwise. Optional: include `Retry-After`.

**Stretch goals:**
- Add `Retry-After` (seconds to next allowed).
- Add global limit (all users), or per-endpoint limits.
- Observability counters (allowed/denied).

## Files

- `app/limiter_memory.py` — In-memory sliding window
- `app/main.py` — FastAPI app wiring both limiters
- `app/config.py` — Settings (pydantic)
- `docker-compose.yml` — Redis service
- `tests/test_limiter.py` — Basic tests
- `tests/test_api.py` — API-level tests (FastAPI)
