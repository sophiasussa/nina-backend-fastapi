from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação usando Pydantic Settings.

    As variáveis são carregadas do arquivo .env ou de variáveis de ambiente.
    """

    # ============================================================
    # Application
    # ============================================================
    PROJECT_NAME: str = "Nina API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # ============================================================
    # Database
    # ============================================================
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/nina_db"

    # ============================================================
    # JWT
    # ============================================================
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ============================================================
    # CORS
    # ============================================================
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
    ]

    # ============================================================
    # Security
    # ============================================================
    BCRYPT_ROUNDS: int = 12



    PASSWORD_RESET_TOKEN_EXPIRE_SECONDS: int = 900
    FRONTEND_URL: str = "https://seuapp.com"



    GOOGLE_CLIENT_ID: str = "seu-client-id.apps.googleusercontent.com"

    # ============================================================
    # Pydantic Settings Config (v2)
    # ============================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna instância única (singleton) das configurações.
    O decorator @lru_cache garante que só será criada uma vez.
    """
    return Settings()


settings = get_settings()
