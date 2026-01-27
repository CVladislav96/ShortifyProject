import pytest
from fastapi.testclient import TestClient


def test_create_short_url_success(client: TestClient):
    """Test for successful creation of a short link"""
    response = client.post(
        "/api/v1/short_url",
        json={"long_url": "https://example.com"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], str)
    assert len(data["data"]) == 6  # Length slug


def test_create_short_url_invalid_url(client: TestClient):
    """Test for creating a short link with an invalid URL"""
    response = client.post(
        "/api/v1/short_url",
        json={"long_url": "not-a-valid-url"}
    )
    
    assert response.status_code == 422  # Validation error


def test_create_short_url_missing_field(client: TestClient):
    """Test creating a short link without a required field"""
    response = client.post(
        "/api/v1/short_url",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


def test_redirect_to_url_success(client: TestClient):
    """Test for successful redirection by slug"""
    # First, create a short link
    create_response = client.post(
        "/api/v1/short_url",
        json={"long_url": "https://example.com/test"}
    )
    
    assert create_response.status_code == 200
    slug = create_response.json()["data"]

    # Now let's check the redirect
    redirect_response = client.get(
        f"/api/v1/{slug}",
        follow_redirects=False
    )
    
    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://example.com/test"


def test_redirect_to_url_not_found(client: TestClient):
    """Redirect test with a non-existent slug"""
    response = client.get(
        "/api/v1/nonexistent",
        follow_redirects=False
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No long url found"


def test_create_multiple_short_urls(client: TestClient):
    """Testing the creation of several short links"""
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    
    slugs = []
    for url in urls:
        response = client.post(
            "/api/v1/short_url",
            json={"long_url": url}
        )
        assert response.status_code == 200
        slugs.append(response.json()["data"])
    
    # We check that all slugs are unique.
    assert len(set(slugs)) == len(slugs)
    
    # We check that all redirects are working.
    for slug, original_url in zip(slugs, urls):
        redirect_response = client.get(
            f"/api/v1/{slug}",
            follow_redirects=False
        )
        assert redirect_response.status_code == 302
        assert redirect_response.headers["location"] == original_url


def test_create_short_url_different_urls(client: TestClient):
    """Test for creating short links for different URLs"""
    url1 = "https://google.com/"
    url2 = "https://github.com/"
    
    response1 = client.post(
        "/api/v1/short_url",
        json={"long_url": url1}
    )
    response2 = client.post(
        "/api/v1/short_url",
        json={"long_url": url2}
    )
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    slug1 = response1.json()["data"]
    slug2 = response2.json()["data"]
    
    # Checking redirects
    redirect1 = client.get(f"/api/v1/{slug1}", follow_redirects=False)
    redirect2 = client.get(f"/api/v1/{slug2}", follow_redirects=False)
    
    assert redirect1.status_code == 302
    assert redirect1.headers["location"] == url1
    assert redirect2.status_code == 302
    assert redirect2.headers["location"] == url2
