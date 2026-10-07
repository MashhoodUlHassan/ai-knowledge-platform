from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Knowledge Platform"
    environment: str = "development"
    debug: bool = True
    allowed_origins: str = "*"

    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "ai_knowledge_platform"
    database_user: str = "postgres"
    database_password: str

    gemini_api_key: str
    gemini_model: str = "gemini-3.8-flash"
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()