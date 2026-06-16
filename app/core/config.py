from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "DevSecOps Trading Platform"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DB_URL: str = "sqlite:///./trading.db"

    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    API_KEY_RED: str = "red-agent-api-key"
    API_KEY_BLUE: str = "blue-agent-api-key"
    API_KEY_INSTITUTIONAL: str = "institutional-agent-api-key"
    API_KEY_RETAIL_A: str = "retail-a-agent-api-key"
    API_KEY_RETAIL_B: str = "retail-b-agent-api-key"

    @property
    def VALID_API_KEYS(self) -> dict:
        return {
            self.API_KEY_RED: "red",
            self.API_KEY_BLUE: "blue",
            self.API_KEY_INSTITUTIONAL: "institutional",
            self.API_KEY_RETAIL_A: "retail_a",
            self.API_KEY_RETAIL_B: "retail_b",
        }

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8000",
    ]

    KRX_DEFAULT_MARKET: str = "KOSPI"
    KRX_CACHE_DIR: str = "data/historical/krx"

    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    WS_HEARTBEAT_INTERVAL: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()