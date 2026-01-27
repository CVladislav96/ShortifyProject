import pytest
from app.services.url_service import generate_short_url, get_url_by_slug
from app.exceptions.url_exceptions import NoLongUrlFoundError


@pytest.mark.asyncio
async def test_generate_short_url_service(setup_test_db):
    """Testing the creation of a short link via the service"""
    long_url = "https://example.com/test"
    
    slug = await generate_short_url(long_url)
    
    assert slug is not None
    assert len(slug) == 6  # Length slug
    assert isinstance(slug, str)


@pytest.mark.asyncio
async def test_get_url_by_slug_service(setup_test_db):
    """Test for obtaining a long link by slug"""
    long_url = "https://example.com/page"
    
    # First, create a short link
    slug = await generate_short_url(long_url)
    
    # Now we get a long link
    retrieved_url = await get_url_by_slug(slug)
    
    assert retrieved_url is not None
    assert retrieved_url == long_url


@pytest.mark.asyncio
async def test_get_url_not_found(setup_test_db):
    """Test for obtaining a long link for a non-existent slug"""
    
    with pytest.raises(NoLongUrlFoundError):
        await get_url_by_slug("nonexistent")


@pytest.mark.asyncio
async def test_slug_uniqueness(setup_test_db):
    """Uniqueness test for generated slugs"""
    
    # Creating several links
    urls = [
        "https://example.com/1",
        "https://example.com/2",
        "https://example.com/3",
    ]
    
    slugs = []
    for url in urls:
        slug = await generate_short_url(url)
        slugs.append(slug)
    
    # Checking uniqueness
    assert len(set(slugs)) == len(slugs)
    assert len(slugs) == 3
