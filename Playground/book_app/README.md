# Book API

A FastAPI-based RESTful API for managing books with CRUD operations, comprehensive testing, JSON logging, and a modern UI.

## Features

- RESTful API with FastAPI
- Modern UI with Jinja2 templates (Bootstrap 5)
- Admin dashboard for managing books
- In-memory database storage (50 books)
- Comprehensive unit and E2E tests (62 tests)
- JSON file logging with daily rotation
- Concurrent request handling with thread-safe ID generation

## Quick Start

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Run the server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Pages

| URL | Description |
|-----|-------------|
| `/` | Home page with featured books |
| `/books` | Browse all books with search & filters |
| `/books/{id}` | Book detail page |
| `/admin` | Admin dashboard for CRUD operations |
| `/docs` | OpenAPI documentation |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/books` | Get all books (optional `?category=` filter) |
| GET | `/api/books/{title}` | Get book by title (case-insensitive) |
| GET | `/api/books/{book_id:int}/details` | Get book by ID |
| POST | `/api/books` | Create a new book |
| PUT | `/api/books/{book_id}` | Update a book |
| DELETE | `/api/books/{book_id}` | Delete a book |

## Project Structure

```
book_app/
├── app/
│   ├── __init__.py       # FastAPI app & logging setup
│   ├── models/           # Pydantic models
│   ├── routes/
│   │   ├── __init__.py   # API routes (/api/books)
│   │   └── ui.py         # UI routes (/, /books, /admin)
│   ├── db/              # In-memory database
│   └── templates/       # Jinja2 HTML templates
│       └── admin/        # Admin dashboard
├── tests/
│   ├── unit/            # Unit tests (models, db)
│   └── e2e/             # E2E tests (API, concurrency)
├── logs/                # JSON log files (auto-generated)
├── AGENTS.md            # Development guide for agents
└── README.md            # This file
```

## Testing

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test file
python -m unittest tests.unit.test_models
python -m unittest tests.e2e.test_api

# Run specific test class
python -m unittest tests.e2e.test_api.TestBooksAPI

# Run specific test method
python -m unittest tests.e2e.test_api.TestBooksAPI.test_create_book_success
```

## Configuration

### Logging

Logs are stored in JSON Lines format in the `logs/` directory:
- Filename format: `app_YYYY-MM-DD.log`
- Rotates daily at midnight
- Log format: `{"timestamp": "...", "level": "INFO", "logger": "app.routes", "message": "..."}`

### Environment

- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
