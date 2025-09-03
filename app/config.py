import os

class Settings:
    LIMIT: int = int(os.getenv("RATE_LIMIT_N", "3"))
    WINDOW_SECONDS: float = float(os.getenv("RATE_LIMIT_T", "10"))
    BACKEND: str = os.getenv("RATE_LIMIT_BACKEND", "memory")  # "memory" or "redis"
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

settings = Settings()
