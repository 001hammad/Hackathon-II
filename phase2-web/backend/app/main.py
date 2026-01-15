"""FastAPI main application instance."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .database.init import create_tables

# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-user todo application API with JWT authentication",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Frontend URLs
    allow_credentials=True,  # Allow cookies and auth headers
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers including Authorization
)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    Creates database tables if they don't exist.
    """
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"Creating database tables...")
    create_tables()
    print(f"Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event handler."""
    print(f"Shutting down {settings.APP_NAME}")


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Register routers
from .routes.auth import router as auth_router
from .routes.tasks import router as tasks_router

app.include_router(auth_router)
app.include_router(tasks_router)
