import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_uri: str = os.environ.get("DATABASE_URL", "sqlite:///./database.db")
    openapi_url: str = os.getenv("OPENAPI_URL", "/openapi.json")
    openapi_prefix: str = ""
    open_market_at = os.getenv("OPEN_MARKET_AT", "06:00")
    close_market_at = os.getenv("CLOSE_MARKET_AT", "15:00")


settings = Settings()
