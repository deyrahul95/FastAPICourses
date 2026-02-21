import logging
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

from fastapi import Body, FastAPI, status, HTTPException

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Book(BaseModel):
    id: int
    title: str
    author: str
    category: str


class AddBookDto(BaseModel):
    title: str = Field(..., description="Book title", min_length=5, max_length=100)
    author: str = Field(..., description="Book author", min_length=2, max_length=50)
    category: str = Field(..., description="Book category", min_length=3, max_length=20)


BOOKS: list[Book] = [
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
    """Increment global book id iterator and return it value"""
    global book_id_iterator
    async with lock:
        book_id_iterator += 1
        return book_id_iterator


@app.get("/books", status_code=status.HTTP_200_OK, response_model=list[Book])
def get_all_books(category: Optional[str] = None) -> list[Book]:
    """Retrieve all books from database optionally filter by category"""
    logger.info("Retrieving books from database...")

    if category is None:
        logger.info(f"Books retrieved successfully. Count: {len(BOOKS)}")
        return BOOKS

    logger.info(f"Filtering books by category: {category}...")
    filter_books: list[Book] = [
        b for b in BOOKS if b.category.casefold() == category.casefold()
    ]
    logger.info(f"Found filter books. Count: {len(filter_books)}")
    return filter_books


@app.get("/books/{title:str}", status_code=status.HTTP_200_OK, response_model=Book)
def get_book(title: str) -> Book:
    """Retrieve single book with search title"""
    logger.info(f"Retrieving book with title: {title}...")

    for book in BOOKS:
        if book.title.casefold() == title.casefold():
            logger.info(
                f"Book found with title: {title}. Id: {book.id}, Author: {book.author}"
            )
            return book

    logger.info(f"No book found with title: {title} in our database")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No book found with title: {title} in our database",
    )


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(request: AddBookDto = Body()) -> Book:
    """Create and add new book into database"""
    id = await increment_book_id()
    logger.info(f"Creating new book... Request: {request}")
    new_book = Book(
        id=id,
        title=request.title,
        author=request.author,
        category=request.category,
    )
    BOOKS.append(new_book)
    logger.info(f"Book created successfully. Book: {new_book}")
    return new_book
