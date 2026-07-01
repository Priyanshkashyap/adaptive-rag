"""
Application settings.
"""

from pydantic_settings import BaseSettings # This is a class that you inherit from to create a settings object that can automatically read values from environment variables, .env files, etc.
from pydantic_settings import SettingsConfigDict #It is simply a configuration dictionary type used to configure how BaseSettings behaves.


class Settings(BaseSettings): # "Create a new class called Settings that inherits all the functionality of BaseSettings."
    """
    Application settings.
    """

    ollama_base_url: str
    ollama_model: str

    tavily_api_key: str

    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str

    mongodb_url: str
    mongodb_database: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings() # type: ignore
