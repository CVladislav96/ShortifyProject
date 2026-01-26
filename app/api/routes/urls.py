from fastapi import APIRouter, status, HTTPException
from fastapi.responses import RedirectResponse

from app.schemas.url import ShortUrlRequest, ShortUrlResponse
from app.services.url_service import generate_short_url, get_url_by_slug
from app.exceptions.url_exceptions import NoLongUrlFoundError

router = APIRouter(prefix="/api/v1", tags=["urls"])


@router.post("/short_url", response_model=ShortUrlResponse)
async def create_short_url(request: ShortUrlRequest):
    new_slug = await generate_short_url(str(request.long_url))
    return ShortUrlResponse(data=new_slug)


@router.get("/{slug}")
async def redirect_to_url(slug: str):
    try:
        long_url = await get_url_by_slug(slug)
    except NoLongUrlFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No long url found"
        )
    return RedirectResponse(url=long_url, status_code=status.HTTP_302_FOUND)
