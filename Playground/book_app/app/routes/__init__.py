import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Body, status, HTTPException
from app.models import Book, AddBookDto, UpdateBookDto
from app.db import (
    increment_book_id,
    get_all_books as db_get_all_books,
    get_book_by_title as db_get_book_by_title,
    get_book_by_id as db_get_book_by_id,
    create_book as db_create_book,
    update_book as db_update_book,
    delete_book as db_delete_book,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/books", tags=["Book"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Book],
)
def get_all_books(category: Optional[str] = None) -> list[Book]:
    """Retrieve all books from the database, optionally filtered by category."""
    logger.info("Retrieving books from database")

    books = db_get_all_books(category)

    logger.info(f"Retrieved {len(books)} book(s)")
    return books


@router.get(
    "/{book_id:int}/details",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def get_book_details(book_id: int) -> Book:
    """Retrieve a book by its unique ID."""
    logger.info(f"Retrieving book with id: {book_id}")

    book = db_get_book_by_id(book_id)
    if not book:
        logger.warning(f"Book not found with id: {book_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} not found",
        )

    logger.info(f"Retrieved book: id={book.id}, title={book.title}")
    return book


@router.get(
    "/{title:str}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def get_book(title: str) -> Book:
    """Retrieve a book by its title (case-insensitive)."""
    logger.info(f"Retrieving book with title: {title}")

    book = db_get_book_by_title(title)
    if not book:
        logger.warning(f"Book not found with title: {title}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with title: {title} not found",
        )

    logger.info(f"Retrieved book: id={book.id}, title={book.title}")
    return book


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
)
async def create_book(request: AddBookDto = Body()) -> Book:
    """Create a new book in the database."""
    logger.info(f"Creating new book: title={request.title}, author={request.author}")

    book_id = await increment_book_id()
    new_book = Book(
        id=book_id,
        title=request.title,
        author=request.author,
        category=request.category,
        updated_at=datetime.now(),
    )
    db_create_book(new_book)

    logger.info(f"Created book: id={new_book.id}, title={new_book.title}")
    return new_book


@router.put(
    "/{book_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_book(book_id: int, request: UpdateBookDto = Body()) -> None:
    """Update an existing book by its ID."""
    logger.info(f"Updating book with id: {book_id}")

    existing_book = db_get_book_by_id(book_id)
    if not existing_book:
        logger.warning(f"Book not found for update: id={book_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} not found",
        )

    if request.title is not None:
        existing_book.title = request.title
    if request.author is not None:
        existing_book.author = request.author
    if request.category is not None:
        existing_book.category = request.category
    existing_book.updated_at = datetime.now()

    db_update_book(book_id, existing_book)
    logger.info(f"Updated book: id={existing_book.id}, title={existing_book.title}")


@router.delete(
    "/{book_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int) -> None:
    """Delete a book by its ID."""
    logger.info(f"Deleting book with id: {book_id}")

    deleted = db_delete_book(book_id)
    if not deleted:
        logger.warning(f"Book not found for deletion: id={book_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id: {book_id} not found",
        )

    logger.info(f"Deleted book with id: {book_id}")
