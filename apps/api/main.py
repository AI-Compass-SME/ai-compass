"""
FastAPI main application.
Entry point for AI-Compass backend API.
"""
import sys
import os
from pathlib import Path

# Add project root to path
api_root = Path(__file__).parent
project_root = api_root.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routers import assessments

# Import questionnaire loader to initialize at startup
from core.questionnaire.loader import get_questionnaire_loader

# Create FastAPI app
app = FastAPI(
    title="AI-Compass API",
    description="AI Maturity Assessment API - Deterministic scoring, ML benchmarking, LLM recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assessments.router, prefix="/api/v1", tags=["assessments"])


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    Loads questionnaire schema on application start.
    """
    try:
        loader = get_questionnaire_loader()
        metadata = loader.get_metadata()
        print(f"✓ Questionnaire loaded: {metadata['questionnaire_id']} v{metadata['questionnaire_version']}")
        print(f"  - Dimensions: {metadata['dimensions_count']}")
        print(f"  - Questions: {metadata['questions_count']}")
        print(f"  - Hash: {metadata['questionnaire_hash'][:12]}...")
    except Exception as e:
        print(f"✗ Failed to load questionnaire: {e}")
        raise


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    Returns API status and questionnaire load status.
    """
    from datetime import datetime
    from db.database import engine
    
    # Check database connection
    db_status = "connected"
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check questionnaire
    questionnaire_loaded = False
    try:
        loader = get_questionnaire_loader()
        questionnaire_loaded = loader._schema is not None
    except:
        pass
    
    return {
        "status": "healthy" if db_status == "connected" and questionnaire_loaded else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "questionnaire_loaded": questionnaire_loaded
    }


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint.
    """
    return {
        "message": "AI-Compass API",
        "version": "1.0.0",
        "docs": "/docs"
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    print(f"Starting AI-Compass API on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)
