from pydantic import BaseModel, HttpUrl


class ShortUrlRequest(BaseModel):
    long_url: HttpUrl


class ShortUrlResponse(BaseModel):
    data: str
