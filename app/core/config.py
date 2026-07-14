"""
Centralized app configuration.
Reads values from environment variables / .env file.
"""
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "RAG Project Chatbot"
    DEBUG: bool = Field(default=True, validation_alias="APP_DEBUG")

    # Database
    DATABASE_URL: str = "sqlite:///./chatbot.db"
    DATABASE_ECHO: bool = False

    # AI provider
    MISTRAL_API_KEY: str = ""
    MISTRAL_MODEL: str = "mistral-small-latest"
    PORT: int = 8000

    # Authentication
    JWT_SECRET_KEY: str = "change-this-development-secret-before-deploying"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*3

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
