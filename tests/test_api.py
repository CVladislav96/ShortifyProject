import pytest
from fastapi.testclient import TestClient


def test_create_short_url_success(client: TestClient):
    """Тест успешного создания короткой ссылки"""
    response = client.post(
        "/api/v1/short_url",
        json={"long_url": "https://example.com"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], str)
    assert len(data["data"]) == 6  # Длина slug


def test_create_short_url_invalid_url(client: TestClient):
    """Тест создания короткой ссылки с невалидным URL"""
    response = client.post(
        "/api/v1/short_url",
        json={"long_url": "not-a-valid-url"}
    )
    
    assert response.status_code == 422  # Validation error


def test_create_short_url_missing_field(client: TestClient):
    """Тест создания короткой ссылки без обязательного поля"""
    response = client.post(
        "/api/v1/short_url",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


def test_redirect_to_url_success(client: TestClient):
    """Тест успешного редиректа по slug"""
    # Сначала создаем короткую ссылку
    create_response = client.post(
        "/api/v1/short_url",
        json={"long_url": "https://example.com/test"}
    )
    
    assert create_response.status_code == 200
    slug = create_response.json()["data"]
    
    # Теперь проверяем редирект
    redirect_response = client.get(
        f"/api/v1/{slug}",
        follow_redirects=False
    )
    
    assert redirect_response.status_code == 302
    assert redirect_response.headers["location"] == "https://example.com/test"


def test_redirect_to_url_not_found(client: TestClient):
    """Тест редиректа с несуществующим slug"""
    response = client.get(
        "/api/v1/nonexistent",
        follow_redirects=False
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "No long url found"


def test_create_multiple_short_urls(client: TestClient):
    """Тест создания нескольких коротких ссылок"""
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
    
    # Проверяем, что все slug уникальны
    assert len(set(slugs)) == len(slugs)
    
    # Проверяем, что все редиректы работают
    for slug, original_url in zip(slugs, urls):
        redirect_response = client.get(
            f"/api/v1/{slug}",
            follow_redirects=False
        )
        assert redirect_response.status_code == 302
        assert redirect_response.headers["location"] == original_url


def test_create_short_url_different_urls(client: TestClient):
    """Тест создания коротких ссылок для разных URL"""
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
    
    # Проверяем редиректы
    redirect1 = client.get(f"/api/v1/{slug1}", follow_redirects=False)
    redirect2 = client.get(f"/api/v1/{slug2}", follow_redirects=False)
    
    assert redirect1.status_code == 302
    assert redirect1.headers["location"] == url1
    assert redirect2.status_code == 302
    assert redirect2.headers["location"] == url2
