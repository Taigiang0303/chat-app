from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import setup_exception_handlers

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Notification service for the Advanced Chat Application",
    version="0.1.0",
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up exception handlers
setup_exception_handlers(app)

# Include routers
# app.include_router(notifications_router, prefix="/api/notifications", tags=["notifications"])
# app.include_router(preferences_router, prefix="/api/preferences", tags=["preferences"])

@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "service": "notification"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 