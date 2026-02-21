import logging
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.db import get_all_books, get_book_by_id, get_categories, search_books

logger = logging.getLogger(__name__)

router = APIRouter(tags=["UI"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with featured books."""
    all_books = get_all_books()
    categories = get_categories()
    featured = all_books[:6]
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "featured_books": featured,
            "categories": categories,
        },
    )


@router.get("/books", response_class=HTMLResponse)
async def books_page(
    request: Request,
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    """Books listing page with filters."""
    categories = get_categories()

    books = get_all_books()
    if category:
        books = [b for b in books if b.category.casefold() == category.casefold()]

    if search:
        books = search_books(search)
        if category:
            books = [b for b in books if b.category.casefold() == category.casefold()]

    return templates.TemplateResponse(
        "books.html",
        {
            "request": request,
            "books": books,
            "categories": categories,
            "selected_category": category,
            "search_query": search,
            "total_books": len(books),
        },
    )


@router.get("/books/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    """Book detail page."""
    book = get_book_by_id(book_id)
    if not book:
        return templates.TemplateResponse(
            "book_detail.html",
            {"request": request, "book": None, "error": "Book not found"},
            status_code=404,
        )
    return templates.TemplateResponse(
        "book_detail.html",
        {"request": request, "book": book},
    )


@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard for managing books."""
    books = get_all_books()
    categories = get_categories()
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "books": books,
            "categories": categories,
            "total_books": len(books),
        },
    )
