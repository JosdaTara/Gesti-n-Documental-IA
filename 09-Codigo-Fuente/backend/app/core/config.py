from functools import lru_cache
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "SIGAD API"
    api_prefix: str = "/api"
    secret_key: str = "cambiar-por-una-clave-larga-y-aleatoria"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24

    database_url: str = "sqlite:///./sigad.db"
    storage_path: str = "./storage"
    demo_mode: bool = True

    openai_api_key: str = ""
    openai_embedding_model: str = "text-embedding-3-small"
    openai_llm_model: str = "gpt-4o-mini"

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _split_origins(cls, value):
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            return ",".join(value)
        return value

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()