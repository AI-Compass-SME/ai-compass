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
    # Updated to handle Prod vs Dev differences
    # Prod: modules/benchmarking_ai/ml_v5
    # Dev (relative to backend): ../../../benchmarking_ai/ml_v5
    ML_MODELS_PATH: str = "modules/benchmarking_ai/ml_v5/model_artifacts/v5"

    @field_validator("ML_MODELS_PATH", mode="before")
    @classmethod
    def set_models_path(cls, v: Any) -> str:
        # Check if we are in Prod (modules folder exists)
        if os.path.exists("modules/benchmarking_ai"):
            return "modules/benchmarking_ai/ml_v5/model_artifacts/v5"
        # Fallback to Dev path (siblings)
        return "../../../benchmarking_ai/ml_v5/model_artifacts/v5"
    
    # CORS
    # We use a string here to avoid Pydantic validation errors with lists from Env vars
    CORS_ORIGINS_STR: str = "http://localhost:5173"

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """
        Parses the CORS_ORIGINS_STR into a list of strings.
        Handles comma-separated values or JSON-like strings.
        """
        if not self.CORS_ORIGINS_STR:
            return []
        
        raw_val = self.CORS_ORIGINS_STR.strip()
        
        if raw_val.startswith("["):
            import json
            try:
                return json.loads(raw_val)
            except json.JSONDecodeError:
                pass # Fallback to comma split

        return [origin.strip() for origin in raw_val.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()
