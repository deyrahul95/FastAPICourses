import asyncio
import copy
from typing import List, Optional

from app.models import Book


def _create_default_books() -> List[Book]:
    """Factory function to create fresh Book instances for default data."""
    return [
        # Self-Help
        Book(id=1, title="Atomic Habits", author="James Clear", category="Self-Help"),
        Book(
            id=2,
            title="The Mountain Is You",
            author="Brianna Wiest",
            category="Self-Help",
        ),
        Book(id=3, title="Can't Hurt Me", author="David Goggins", category="Self-Help"),
        Book(id=4, title="The 5 AM Club", author="Robin Sharma", category="Self-Help"),
        Book(
            id=5,
            title="Think and Grow Rich",
            author="Napoleon Hill",
            category="Self-Help",
        ),
        Book(
            id=6, title="The Power of Now", author="Eckhart Tolle", category="Self-Help"
        ),
        Book(
            id=7,
            title="How to Win Friends and Influence People",
            author="Dale Carnegie",
            category="Self-Help",
        ),
        Book(
            id=8,
            title="The Seven Habits of Highly Effective People",
            author="Stephen Covey",
            category="Self-Help",
        ),
        Book(id=9, title="Deep Work", author="Cal Newport", category="Self-Help"),
        Book(id=10, title="Atomic Habits", author="James Clear", category="Self-Help"),
        # Motivational
        Book(
            id=11,
            title="The Gifts of Imperfection",
            author="Brené Brown",
            category="Motivational",
        ),
        Book(
            id=12,
            title="The Daily Stoic",
            author="Ryan Holiday",
            category="Motivational",
        ),
        Book(
            id=13,
            title="Awaken the Giant Within",
            author="Tony Robbins",
            category="Motivational",
        ),
        Book(id=14, title="Relentless", author="Tim Grover", category="Motivational"),
        Book(
            id=15,
            title="The Four Agreements",
            author="Don Miguel Ruiz",
            category="Motivational",
        ),
        Book(
            id=16,
            title="Mindset: The New Psychology of Success",
            author="Carol Dweck",
            category="Motivational",
        ),
        Book(id=17, title="Drive", author="Daniel Pink", category="Motivational"),
        Book(
            id=18,
            title="The Compound Effect",
            author="Darren Hardy",
            category="Motivational",
        ),
        Book(
            id=19, title="Unshakeable", author="Tony Robbins", category="Motivational"
        ),
        Book(
            id=20,
            title="You Are a Badass",
            author="Jen Sincero",
            category="Motivational",
        ),
        # Leadership
        Book(
            id=21, title="Start With Why", author="Simon Sinek", category="Leadership"
        ),
        Book(id=22, title="Good to Great", author="Jim Collins", category="Leadership"),
        Book(
            id=23, title="The Lean Startup", author="Eric Ries", category="Leadership"
        ),
        Book(id=24, title="Zero to One", author="Peter Thiel", category="Leadership"),
        Book(
            id=25,
            title="The Hard Thing About Hard Things",
            author="Ben Horowitz",
            category="Leadership",
        ),
        Book(
            id=26, title="Leaders Eat Last", author="Simon Sinek", category="Leadership"
        ),
        Book(
            id=27,
            title="The Innovator's Dilemma",
            author="Clayton Christensen",
            category="Leadership",
        ),
        Book(
            id=28, title="Playing to Win", author="A.G. Lafley", category="Leadership"
        ),
        Book(id=29, title="Scaling Up", author="Verne Harnish", category="Leadership"),
        Book(
            id=30,
            title="Trillion Dollar Coach",
            author="Eric Schmidt",
            category="Leadership",
        ),
        # Philosophy
        Book(
            id=31, title="Meditations", author="Marcus Aurelius", category="Philosophy"
        ),
        Book(id=32, title="The Art of War", author="Sun Tzu", category="Philosophy"),
        Book(
            id=33,
            title="48 Laws of Power",
            author="Robert Greene",
            category="Philosophy",
        ),
        Book(
            id=34,
            title="The Prince",
            author="Niccolò Machiavelli",
            category="Philosophy",
        ),
        Book(
            id=35,
            title="Man's Search for Meaning",
            author="Viktor Frankl",
            category="Philosophy",
        ),
        Book(
            id=36,
            title="The Subtle Art of Not Giving a F*ck",
            author="Mark Manson",
            category="Philosophy",
        ),
        Book(
            id=37, title="The Alchemist", author="Paulo Coelho", category="Philosophy"
        ),
        Book(id=38, title="Sapiens", author="Yuval Noah Harari", category="Philosophy"),
        Book(
            id=39,
            title="12 Rules for Life",
            author="Jordan Peterson",
            category="Philosophy",
        ),
        Book(
            id=40,
            title="Man Search for Himself",
            author="Rollo May",
            category="Philosophy",
        ),
        # Business
        Book(id=41, title="Zero to One", author="Blake Masters", category="Business"),
        Book(
            id=42,
            title="Blue Ocean Strategy",
            author="W. Chan Kim",
            category="Business",
        ),
        Book(
            id=43,
            title="Crossing the Chasm",
            author="Geoffrey Moore",
            category="Business",
        ),
        Book(id=44, title="The Purple Cow", author="Seth Godin", category="Business"),
        Book(id=45, title="Hooked", author="Nir Eyal", category="Business"),
        Book(
            id=46,
            title="The Ultimate Sales Machine",
            author="Chet Holmes",
            category="Business",
        ),
        Book(
            id=47,
            title="Predictably Irrational",
            author="Dan Ariely",
            category="Business",
        ),
        Book(
            id=48,
            title="The New New Thing",
            author="Michael Lewis",
            category="Business",
        ),
        Book(
            id=49,
            title="The Black Swan",
            author="Nassim Nicholas Taleb",
            category="Business",
        ),
        Book(
            id=50, title="The Personal MBA", author="Josh Kaufman", category="Business"
        ),
    ]


BOOKS: List[Book] = _create_default_books()
book_id_iterator: int = 100
lock = asyncio.Lock()


def reset_books() -> None:
    """Reset the in-memory database to its initial state. Used for testing."""
    global BOOKS, book_id_iterator
    BOOKS.clear()
    BOOKS.extend(copy.deepcopy(_create_default_books()))
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


def get_categories() -> List[str]:
    """Get all unique categories from the database."""
    return sorted(set(book.category for book in BOOKS))


def search_books(query: str) -> List[Book]:
    """Search books by title or author (case-insensitive)."""
    query_lower = query.lower()
    return [
        book
        for book in BOOKS
        if query_lower in book.title.lower() or query_lower in book.author.lower()
    ]


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
