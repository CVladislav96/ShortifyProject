from contextlib import asynccontextmanager

from fastapi import Body, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse

from database.db import engine
from database.models import Base
from exceptions import NoLongUrlFoundError

from service import generate_short_url, get_url_by_slug


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/short_url")
async def generate_slug(
    long_url: str = Body(embed=True)
):
    new_slug = await generate_short_url(long_url)
    return {"data": new_slug}

@app.get("/{slug}")
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except NoLongUrlFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No long url found")
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)


