import logging

# Configure logging to show up in Render logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting Application Init...")

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from config import get_settings
    from routers import api_router
    logger.info("Imports successful")
except Exception as e:
    logger.error(f"Error during imports: {e}")
    raise e

try:
    settings = get_settings()
    logger.info(f"Settings loaded. Project: {settings.PROJECT_NAME}")
except Exception as e:
    logger.error(f"Error loading settings: {e}")
    raise e

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Includes
try:
    app.include_router(api_router, prefix=settings.API_V1_STR)
    logger.info("API Router included")
except Exception as e:
    logger.error(f"Error including router: {e}")
    raise e

# CORS
if settings.CORS_ORIGINS:
    try:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(f"CORS enabled for: {settings.CORS_ORIGINS}")
    except Exception as e:
        logger.error(f"Error setting up CORS: {e}")
        raise e

@app.get("/")
def root():
    logger.info("Health check endpoint hit")
    return {"message": "Welcome to AI-Compass API", "docs": "/docs", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
