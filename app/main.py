from fastapi import FastAPI, HTTPException, Query

from app.config import settings
from app.limiter_memory import SlidingWindowLimiter as MemLimiter

app = FastAPI(title="Distributed Rate Limiter Interview")


limiter = MemLimiter(settings.LIMIT, settings.WINDOW_SECONDS)


@app.get("/ping")
def ping(user_id: str = Query(..., min_length=1)):
    if limiter.allow(user_id):
        return {"ok": True, "user_id": user_id}
    else:
        retry = getattr(limiter, "retry_after", lambda uid: 1.0)(user_id)
        raise HTTPException(
            status_code=429,
            detail="rate_limited",
            headers={"Retry-After": str(int(retry) + 1)},
        )
