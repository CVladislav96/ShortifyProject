# Shortify - URL Shortener Application

A modern, full-stack URL shortening service built with FastAPI backend and responsive frontend. Shortify allows you to create short, shareable links from long URLs.

## 🌟 Features

- **URL Shortening**: Convert long URLs into concise, memorable short codes
- **Custom Slugs**: Optionally provide custom short codes for URLs
- **Automatic Redirects**: Seamless redirect from short code to original URL
- **Database Storage**: Persistent storage using SQLite/PostgreSQL
- **RESTful API**: Well-documented API endpoints with FastAPI
- **Modern Frontend**: Responsive web interface built with HTML/CSS/JavaScript
- **Development Friendly**: Docker support with docker-compose for easy setup

## 📋 Project Structure

```
ShortifyProject/
├── app/                      # Backend application (FastAPI)
│   ├── api/
│   │   └── routes/
│   │       └── urls.py      # URL endpoints
│   ├── core/
│   │   ├── config.py        # Configuration
│   │   └── database.py      # Database setup
│   ├── models/
│   │   └── url.py           # URL data model
│   ├── repositories/
│   │   └── url_repository.py # Data access layer
│   ├── schemas/
│   │   └── url.py           # Pydantic schemas
│   ├── services/
│   │   └── url_service.py   # Business logic
│   ├── exceptions/
│   │   └── url_exceptions.py # Custom exceptions
│   ├── utils/
│   │   └── slug_generator.py # Slug generation utility
│   └── main.py              # FastAPI application entry
├── frontend/                 # Frontend application
│   ├── index.html           # Main page
│   ├── redirect.html        # Redirect page
│   ├── dev_server.py        # Development server
│   ├── nginx.conf           # Production nginx config
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── api.js           # API client
│       └── app.js           # Main app logic
├── tests/                   # Test suite
│   ├── test_api.py
│   ├── test_service.py
│   └── conftest.py
├── docker-compose.yaml      # Docker services configuration
├── pyproject.toml          # Python project configuration
├── pytest.ini              # Pytest configuration
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose (optional, for containerized setup)

### Local Development Setup

1. **Clone the repository**
   ```bash
   cd ShortifyProject
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e .
   ```

4. **Start the backend**
   ```bash
   cd app
   uvicorn main:app --reload
   ```
   The API will be available at `http://localhost:8000`
   API documentation: `http://localhost:8000/docs`

5. **Start the frontend** (in another terminal)
   ```bash
   cd frontend
   python dev_server.py
   ```
   The frontend will be available at `http://localhost:8080`

### Docker Setup (Production)

```bash
docker-compose up -d
```

This will start both the backend API and frontend services.

## 📖 API Documentation

### Create a Short URL

**Endpoint:** `POST /api/urls`

**Request:**
```json
{
  "original_url": "https://example.com/very/long/url",
  "custom_slug": "my-short-link"  # Optional
}
```

**Response:**
```json
{
  "id": 1,
  "original_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "custom_slug": "my-short-link",
  "created_at": "2026-01-28T10:30:00Z",
  "click_count": 0
}
```

### Redirect to Original URL

**Endpoint:** `GET /{short_code}`

Automatically redirects to the original URL and increments the click counter.

### Get URL Details

**Endpoint:** `GET /api/urls/{short_code}`

Returns information about a shortened URL including click statistics.

### List All URLs

**Endpoint:** `GET /api/urls`

Returns a list of all shortened URLs with pagination support.

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

Run specific test file:

```bash
pytest tests/test_api.py
```

## 🔧 Configuration

Configuration is managed through `app/core/config.py`. Key settings:

- `DATABASE_URL`: Database connection string
- `API_TITLE`: API title shown in documentation
- `CORS_ORIGINS`: Allowed CORS origins
- `SLUG_LENGTH`: Default length for generated slugs

## 📝 Development

### Code Style

The project uses Black for code formatting:

```bash
black app/ tests/
```

### Type Checking

Uses Pydantic for validation and type hints throughout the codebase.

### Database Migrations

Currently using SQLAlchemy Core. For schema changes:

1. Update the model in `app/models/url.py`
2. Tables are auto-created on application startup via `Base.metadata.create_all()`

## 🌐 Frontend

The frontend is a single-page application (SPA) that provides:

- **URL Shortening Form**: Simple interface to create short links
- **Link Management**: View, copy, and delete shortened URLs
- **Statistics**: Click tracking for each shortened URL
- **Auto-Redirect**: Direct short URL redirects to original destination

See [frontend/README.md](frontend/README.md) for detailed frontend documentation.

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.12+ is installed: `python --version`
- Check that all dependencies are installed: `pip install -e .`
- Verify the database configuration in `app/core/config.py`

### Frontend can't connect to API
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in `app/main.py`
- Verify API endpoint in `frontend/js/api.js`

### Database errors
- Check that the database file/service is accessible
- Review logs in `app/core/database.py`

## 📦 Dependencies

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM and database toolkit
- **Pydantic**: Data validation
- **Uvicorn**: ASGI server
- **httpx**: HTTP client
- **aiosqlite/asyncpg**: Async database drivers

### Development
- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **black**: Code formatter

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ **Commercial use**: You can use this software for commercial purposes
- ✅ **Modification**: You can modify the software
- ✅ **Distribution**: You can distribute the software
- ✅ **Private use**: You can use this software privately
- ⚠️ **Liability**: The software is provided "as is", without warranty
- ⚠️ **Copyright**: Must include the original copyright notice

For the full license text, please refer to the [LICENSE](LICENSE) file in the repository.

---

**Last Updated:** January 30, 2026
