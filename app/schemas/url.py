from pydantic import BaseModel, HttpUrl


class ShortUrlRequest(BaseModel):
    long_url: HttpUrl


class ShortURLData(BaseModel):
    short_code: str
    long_url: str


class ShortUrlResponse(BaseModel):
    data: ShortURLData
