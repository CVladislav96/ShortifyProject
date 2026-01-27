import pytest
import sys
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

# Test database (in-memory SQLite for tests)
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

# Redefine database modules BEFORE importing models
import app.core.database as db_module
db_module.engine = test_engine
db_module.new_session = TestSessionLocal

# NOW we import the models and the rest
from app.models.url import Base
from app.api.routes import urls


@pytest.fixture(scope="function")
async def setup_test_db():
    """Creates a test database and clears it after each test"""
    # Creating tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    # Delete tables after testing
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_app(setup_test_db):
    """Creates a test application"""
    app = FastAPI(
        title="Shortify API Test",
        description="URL Shortener Service - Test",
        version="0.1.0"
    )
    app.include_router(urls.router)
    return app


@pytest.fixture(scope="function")
def client(test_app):
    """Creates a test client for synchronous tests"""
    return TestClient(test_app)
