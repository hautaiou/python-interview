# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup
```bash
uv sync  # Install dependencies and create virtual environment
```

### Running the Application
```bash
# Local (in-memory limiter)
uv run uvicorn app.main:app --reload

# With Redis backend
docker compose up -d
export RATE_LIMIT_BACKEND=redis
export REDIS_URL=redis://localhost:6379/0
uv run uvicorn app.main:app --reload
```

### Testing
```bash
uv run pytest -q                           # Run all tests quietly
uv run pytest tests/test_limiter.py        # Run specific test file
uv run pytest tests/test_api.py::test_api_ping_ok_until_limited  # Run single test
```

### Manual Testing
```bash
curl -i 'http://127.0.0.1:8000/ping?user_id=alice'
```

## Architecture

### Rate Limiter System Design
The codebase implements a pluggable rate limiting architecture with two backends:

1. **In-Memory Backend** (`app/limiter_memory.py`): 
   - `SlidingWindowLimiter` class for single-instance deployments
   - Currently returns `True` for all requests (stub implementation)
   - Intended to track request timestamps per user in sliding time windows

2. **Redis Backend** (referenced but not yet implemented):
   - Distributed rate limiting using Redis for multi-instance deployments
   - Should use atomic Lua scripts for race-condition-free operations
   - Key design considerations: TTL-based cleanup, clock skew mitigation

### Application Structure
- **FastAPI App** (`app/main.py`): Single `/ping` endpoint that applies rate limiting
- **Configuration** (`app/config.py`): Pydantic settings with defaults (3 requests per 10 seconds)
- **Dependency Management**: Uses `pyproject.toml` with FastAPI, Redis, and testing dependencies

### Key Implementation Details
- Rate limiter returns boolean (allow/deny) from `allow(user_id: str)` method
- 429 responses include `Retry-After` header calculated from `retry_after()` method
- Settings are environment-configurable via pydantic-settings
- Docker Compose provides Redis 9 Alpine with persistence enabled

### Testing Strategy
- Unit tests for rate limiter logic in `tests/test_limiter.py`
- Integration tests for FastAPI endpoints in `tests/test_api.py`
- Tests verify both allow/deny behavior and proper HTTP status codes/headers