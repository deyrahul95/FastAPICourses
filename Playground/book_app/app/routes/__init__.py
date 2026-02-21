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

router = APIRouter(prefix="/books", tags=["Book"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[Book],
)
def get_all_books(category: Optional[str] = None) -> list[Book]:
    logger.info("Retrieving books from database...")

    books = db_get_all_books(category)

    logger.info(f"Books retrieved successfully. Count: {len(books)}")
    return books


@router.get(
    "/{title:str}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def get_book(title: str) -> Book:
    logger.info(f"Retrieving book with title: {title}...")

    book = db_get_book_by_title(title)
    if book:
        logger.info(
            f"Book found with title: {title}. Id: {book.id}, Author: {book.author}"
        )
        return book

    logger.info(f"No book found with title: {title} in our database")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No book found with title: {title} in our database",
    )


@router.get(
    "/{book_id:int}/details",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def get_book_details(book_id: int) -> Book:
    logger.info(f"Retrieving book with id: {book_id}...")

    book = db_get_book_by_id(book_id)
    if book:
        logger.info(f"Book found successfully. Id: {book.id}, Title: {book.title}")
        return book

    logger.info(f"No book found with id: {book_id} in our database")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No book found with id: {book_id} in our database",
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
)
async def create_book(request: AddBookDto = Body()) -> Book:
    book_id = await increment_book_id()
    logger.info(f"Creating new book... Request: {request}")
    new_book = Book(
        id=book_id,
        title=request.title,
        author=request.author,
        category=request.category,
        updated_at=datetime.now(),
    )
    db_create_book(new_book)
    logger.info(f"Book created successfully. Book: {new_book}")
    return new_book


@router.put(
    "/{book_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_book(book_id: int, request: UpdateBookDto = Body()) -> None:
    logger.info(f"Updating book ... BookId: {book_id}, Request: {request}")

    existing_book = db_get_book_by_id(book_id)
    if not existing_book:
        logger.info(f"Book with id:{book_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id:{book_id} not found in database",
        )

    existing_book.title = (
        request.title if request.title is not None else existing_book.title
    )
    existing_book.author = (
        request.author if request.author is not None else existing_book.author
    )
    existing_book.category = (
        request.category if request.category is not None else existing_book.category
    )
    existing_book.updated_at = datetime.now()

    db_update_book(book_id, existing_book)
    logger.info(f"Book updated successfully. Book: {existing_book}")


@router.delete(
    "/{book_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int) -> None:
    logger.info(f"Deleting book with id: {book_id}...")

    deleted = db_delete_book(book_id)
    if not deleted:
        logger.info(f"Book with id:{book_id} not found in database")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id:{book_id} not found in database",
        )

    logger.info("Book deleted successfully.")
