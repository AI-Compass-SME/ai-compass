import os
from pydantic_settings import BaseSettings
from functools import lru_cache

from typing import Any, Union, List, Annotated
from pydantic import BeforeValidator

def parse_cors(v: Any) -> List[str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI-Compass API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    
    # ML Models
    ML_MODELS_PATH: str = "../benchmarking_ai/ml_v5/model_artifacts/v5"
    
    # CORS
    CORS_ORIGINS: Annotated[List[str], BeforeValidator(parse_cors)] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
