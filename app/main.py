from contextlib import asynccontextmanager
from fastapi import FastAPI

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

app.include_router(urls.router)
