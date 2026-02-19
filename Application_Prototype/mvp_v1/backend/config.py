import os
from pydantic_settings import BaseSettings
from functools import lru_cache

from typing import Any, Union
from pydantic import field_validator

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

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
