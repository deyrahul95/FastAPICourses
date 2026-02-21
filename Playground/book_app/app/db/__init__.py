import asyncio
from typing import List, Optional

from app.models import Book


BOOKS: List[Book] = [
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

book_id_iterator: int = 100
lock = asyncio.Lock()


async def increment_book_id() -> int:
    global book_id_iterator
    async with lock:
        book_id_iterator += 1
        return book_id_iterator


def get_all_books(category: Optional[str] = None) -> List[Book]:
    if category is None:
        return BOOKS
    return [b for b in BOOKS if b.category.casefold() == category.casefold()]


def get_book_by_title(title: str) -> Optional[Book]:
    for book in BOOKS:
        if book.title.casefold() == title.casefold():
            return book
    return None


def get_book_by_id(book_id: int) -> Optional[Book]:
    for book in BOOKS:
        if book.id == book_id:
            return book
    return None


def create_book(book: Book) -> Book:
    BOOKS.append(book)
    return book


def update_book(book_id: int, book: Book) -> bool:
    for i, b in enumerate(BOOKS):
        if b.id == book_id:
            BOOKS[i] = book
            return True
    return False


def delete_book(book_id: int) -> bool:
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            return True
    return False
