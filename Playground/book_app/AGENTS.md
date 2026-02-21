# AGENTS.md - Book App Development Guide

## Project Overview

This is a FastAPI-based book management application with CRUD operations for books. The app uses in-memory storage and includes concurrency testing.

## Running the Application

```bash
# Start the FastAPI server (development)
uvicorn books:app --reload --host 0.0.0.0 --port 8000

# Or run directly with Python
python -m uvicorn books:app --reload
```

## Testing

### Run All Tests

```bash
# Using unittest
python -m unittest discover -s . -p "*_test.py"

# Or run the test file directly
python books_test.py
```

### Run a Single Test

```bash
# Run a specific test class
python -m unittest books_test.TestConcurrency

# Run a specific test method
python -m unittest books_test.TestConcurrency.test_concurrent_requests
```

## Code Style Guidelines

### Imports

- Standard library imports first (`logging`, `asyncio`, `typing`)
- Third-party imports second (`pydantic`, `fastapi`)
- Use explicit imports (avoid `from x import *`)
- Group imports by type with blank lines between groups

### Formatting

- Maximum line length: 100 characters (soft limit: 120)
- Use 4 spaces for indentation (not tabs)
- Add blank lines between class/function definitions (2 lines)
- Use trailing commas in multi-line collections

### Type Annotations

- Always use type hints for function parameters and return types
- Use built-in types directly (`list`, `dict`, `Optional`) in type hints
- Use `typing` module for complex types when Python < 3.9

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `Book`, `AddBookDto`)
- **Functions/variables**: `snake_case` (e.g., `get_all_books`, `book_id_iterator`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `BOOKS`)
- **Private members**: Prefix with underscore (e.g., `_internal_value`)

### Pydantic Models

- Use `BaseModel` for DTOs and data transfer objects
- Use `Field()` with `description` for documentation
- Use `Optional[]` with `default=None` for optional fields
- Add validation constraints (`min_length`, `max_length`, etc.)

### Error Handling

- Use `HTTPException` for HTTP errors with appropriate status codes
- Include descriptive error messages in `detail`
- Log errors before raising exceptions

### Logging

- Use the standard `logging` module
- Create logger with `logger = logging.getLogger(__name__)`
- Log at appropriate levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`
- Include contextual information in log messages

### API Design

- Use appropriate HTTP methods: `GET` (retrieve), `POST` (create), `PUT` (update), `DELETE` (remove)
- Use proper status codes: `200` (OK), `201` (Created), `204` (No Content), `404` (Not Found)
- Use `response_model` for type validation in responses
- Group endpoints with `tags` parameter

### Async/Await

- Use `async def` for route handlers that perform async operations
- Use `asyncio.Lock()` for thread-safe operations on shared state
- Prefer async patterns over threading where possible

### Testing

- Use `unittest` framework
- Use `TestClient` from `fastapi.testclient` for API testing
- Use `setUp` method to initialize test fixtures
- Test concurrency with threading for race condition detection

## Project Structure

```
book_app/
├── app/
│   ├── __init__.py       # FastAPI app factory (create_app())
│   ├── models/
│   │   └── __init__.py   # Book, AddBookDto, UpdateBookDto
│   ├── routes/
│   │   └── __init__.py   # Book API endpoints
│   └── db/
│       └── __init__.py   # In-memory storage & operations
├── tests/
│   ├── __init__.py
│   └── test_books.py     # Unit tests
└── AGENTS.md             # Development guide
```

## Running the Application

```bash
# Start the FastAPI server
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -p "test_*.py"

# Run specific test
python -m unittest tests.test_books.TestConcurrency
```

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- `python-multipart` - Form parsing (optional, for file uploads)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books` | Retrieve all books, optional `category` filter |
| GET | `/books/{title}` | Get book by title (case-insensitive) |
| GET | `/books/{book_id:int}/details` | Get book details by ID |
| POST | `/books` | Create new book (returns 201) |
| PUT | `/books/{book_id}` | Update book (returns 204) |
| DELETE | `/books/{book_id}` | Delete book (returns 204) |

## Data Models

### Book (Response Model)
```python
class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str
    updated_at: datetime
```

### AddBookDto (Request Model)
- `title`: string, required, 5-100 characters
- `author`: string, required, 2-50 characters
- `category`: string, required, 3-20 characters

### UpdateBookDto (Request Model)
- All fields optional with `None` default
- Same validation constraints as AddBookDto

## Common Patterns

### Adding a New Endpoint
1. Import necessary modules (FastAPI, status, HTTPException)
2. Use appropriate decorator (`@app.get`, `@app.post`, etc.)
3. Define request/response models using Pydantic
4. Add proper status codes and `response_model`
5. Group with `tags=["Book"]` for documentation
6. Add logging at INFO level for operations

### Adding a New Test
1. Import `unittest` and `TestClient` from `fastapi.testclient`
2. Create a new test class inheriting from `unittest.TestCase`
3. Use `setUp` method to initialize `TestClient`
4. Write test methods with `self.assert*` assertions
5. For concurrency tests, use `threading.Thread`

## Things to Avoid

- Do not commit secrets, API keys, or credentials to the repository
- Do not use `print()` for debugging (use `logging` module instead)
- Do not use bare `except:` clauses - catch specific exceptions
- Do not modify the global `BOOKS` list without proper locking in async contexts
- Do not skip error handling in route handlers
- Do not forget to add type annotations to new functions

## Development Workflow

1. **Run tests** before committing: `python -m unittest books_test`
2. **Start server** for manual testing: `uvicorn books:app --reload`
3. **Test API** at `http://localhost:8000/docs` (Swagger UI)
4. **Verify** all endpoints work correctly after changes

## Version

- Python: 3.9+ (uses built-in types like `list` in type hints)
- FastAPI: Latest compatible version
- Pydantic: v2+ (uses `Field` with constraints)
