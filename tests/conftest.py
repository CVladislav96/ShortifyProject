import pytest
import sys
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Тестовая БД (in-memory SQLite для тестов)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
)

# Переопределяем модули БД ПЕРЕД импортом моделей
import app.core.database as db_module
db_module.engine = test_engine
db_module.new_session = TestSessionLocal

# ТЕПЕРЬ импортируем модели и остальное
from app.models.url import Base
from app.api.routes import urls


@pytest.fixture(scope="function")
async def setup_test_db():
    """Создает тестовую БД и очищает её после каждого теста"""
    # Создаем таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Удаляем таблицы после теста
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_app(setup_test_db):
    """Создает тестовое приложение"""
    app = FastAPI(
        title="Shortify API Test",
        description="URL Shortener Service - Test",
        version="0.1.0"
    )
    app.include_router(urls.router)
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """Создает тестовый клиент для синхронных тестов"""
    return TestClient(test_app)
