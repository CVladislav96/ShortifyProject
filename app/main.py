from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import engine
from app.core.config import settings
from app.models.url import Base
from app.api.routes import urls
from app.middleware.rate_limiter import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware, calls=settings.rate_limit_calls, period=settings.rate_limit_period)

app.include_router(urls.router)
app.include_router(urls.router, prefix="")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.environment}

# Serve frontend files
frontend_path = Path(__file__).parent.parent / "frontend"

# Mount frontend static files (CSS, JS, etc.)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
