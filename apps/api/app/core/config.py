from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )

    app_env: str = "development"
    app_name: str = "HelaCare API"
    api_prefix: str = "/api/v1"

    database_url: str = (
        "postgresql+asyncpg://helacare:"
        "helacare_dev_password@db:5432/helacare"
    )

    database_url_sync: str = (
        "postgresql+psycopg://helacare:"
        "helacare_dev_password@db:5432/helacare"
    )

    redis_url: str = "redis://redis:6379/0"

    admin_email: str = "admin@helacare.local"
    admin_password: str = "change-me-now"
    jwt_secret: str = "change-this-development-secret"
    jwt_algorithm: str = "HS256"
    jwt_exp_minutes: int = 480

    rag_enabled: bool = True
    rag_vector_dimensions: int = 256

    # Keep this as a simple string so Docker/Pydantic
    # do not try to decode it as JSON.
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()