import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Compass API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # ML Models
    ML_MODELS_PATH: str = "../benchmarking_ai/ml_v5/model_artifacts/v5"
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        # Since the .env is in the root project folder (../../), we might need to point to it explicitly
        # or rely on the environment being loaded before running the app.
        # For now, we'll assume the .env is loaded or copied to backend.
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
