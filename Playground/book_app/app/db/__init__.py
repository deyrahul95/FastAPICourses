import asyncio
from typing import List, Optional

from app.models import Book


DEFAULT_BOOKS: List[Book] = [
    Book(id=1, title="Atomic Habits", author="James Clear", category="Self-Help"),
    Book(
        id=2,
        title="The Gifts of Imperfection",
        author="Brené Brown",
        category="Motivational",
    ),
    Book(
        id=3, title="The Mountain Is You", author="Brianna Wiest", category="Self-Help"
    ),
    Book(id=4, title="The Daily Stoic", author="Ryan Holiday", category="Motivational"),
    Book(id=5, title="Start With Why", author="Simon Sinek", category="Logical"),
]

BOOKS: List[Book] = DEFAULT_BOOKS.copy()
book_id_iterator: int = 100
lock = asyncio.Lock()


def reset_books() -> None:
    """Reset the in-memory database to its initial state. Used for testing."""
    global BOOKS, book_id_iterator
    BOOKS.clear()
    BOOKS.extend(DEFAULT_BOOKS.copy())
    book_id_iterator = 100


async def increment_book_id() -> int:
    """Atomically increment and return the next available book ID."""
    global book_id_iterator
    async with lock:
        book_id_iterator += 1
        return book_id_iterator


def get_all_books(category: Optional[str] = None) -> List[Book]:
    """Retrieve all books, optionally filtered by category (case-insensitive)."""
    if category is None:
        return BOOKS.copy()
    return [book for book in BOOKS if book.category.casefold() == category.casefold()]


def get_book_by_title(title: str) -> Optional[Book]:
    """Find a book by its title (case-insensitive)."""
    for book in BOOKS:
        if book.title.casefold() == title.casefold():
            return book
    return None


def get_book_by_id(book_id: int) -> Optional[Book]:
    """Find a book by its unique ID."""
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None


def create_book(book: Book) -> Book:
    """Add a new book to the database."""
    BOOKS.append(book)
    return book


def update_book(book_id: int, book: Book) -> bool:
    """Update an existing book by ID. Returns True if successful."""
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book_id:
            BOOKS[i] = book
            return True
    return False


def delete_book(book_id: int) -> bool:
    """Delete a book by ID. Returns True if the book was found and deleted."""
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            return True
    return False
