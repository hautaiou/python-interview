from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    LIMIT: int = 3
    WINDOW_SECONDS: float = 10.0


settings = Settings()
