# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path

class Settings(BaseSettings):
    mistral_api_key: str
    mistral_model: str

    deezer_base_url: str = "https://api.deezer.com"

    class Config:
        env_file = Path(__file__).resolve().parent / ".env" 
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
