from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException

from app.core.database import engine
from app.models.url import Base
from app.api.routes import urls


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Shortify API",
    description="URL Shortener Service",
    version="0.1.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(urls.router)
app.include_router(urls.router, prefix="")

# Serve frontend files
frontend_path = Path(__file__).parent.parent / "frontend"

# Mount frontend static files (CSS, JS, etc.)
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
