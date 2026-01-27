import pytest
from app.services.url_service import generate_short_url, get_url_by_slug
from app.exceptions.url_exceptions import NoLongUrlFoundError


@pytest.mark.asyncio
async def test_generate_short_url_service(setup_test_db):
    """Тест создания короткой ссылки через сервис"""
    long_url = "https://example.com/test"
    
    slug = await generate_short_url(long_url)
    
    assert slug is not None
    assert len(slug) == 6  # Длина slug
    assert isinstance(slug, str)


@pytest.mark.asyncio
async def test_get_url_by_slug_service(setup_test_db):
    """Тест получения длинной ссылки по slug"""
    long_url = "https://example.com/page"
    
    # Сначала создаем короткую ссылку
    slug = await generate_short_url(long_url)
    
    # Теперь получаем длинную ссылку
    retrieved_url = await get_url_by_slug(slug)
    
    assert retrieved_url is not None
    assert retrieved_url == long_url


@pytest.mark.asyncio
async def test_get_url_not_found(setup_test_db):
    """Тест получения длинной ссылки для несуществующего slug"""
    
    with pytest.raises(NoLongUrlFoundError):
        await get_url_by_slug("nonexistent")


@pytest.mark.asyncio
async def test_slug_uniqueness(setup_test_db):
    """Тест уникальности сгенерированных slug"""
    
    # Создаем несколько ссылок
    urls = [
        "https://example.com/1",
        "https://example.com/2",
        "https://example.com/3",
    ]
    
    slugs = []
    for url in urls:
        slug = await generate_short_url(url)
        slugs.append(slug)
    
    # Проверяем уникальность
    assert len(set(slugs)) == len(slugs)
    assert len(slugs) == 3
