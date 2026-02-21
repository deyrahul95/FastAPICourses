import unittest
from app.models import Book
from app.db import (
    get_all_books,
    get_book_by_title,
    get_book_by_id,
    create_book,
    update_book,
    delete_book,
    reset_books,
    BOOKS,
)


class TestDatabaseFunctions(unittest.TestCase):
    """Unit tests for the database layer functions."""

    def setUp(self):
        """Reset database before each test."""
        reset_books()

    def test_get_all_books_returns_all(self):
        """Test that get_all_books returns all books when no filter."""
        books = get_all_books()
        self.assertEqual(len(books), 5)
        self.assertEqual(books[0].title, "Atomic Habits")

    def test_get_all_books_with_category_filter(self):
        """Test filtering books by category (case-insensitive)."""
        books = get_all_books("self-help")
        self.assertEqual(len(books), 2)
        for book in books:
            self.assertEqual(book.category.casefold(), "self-help")

    def test_get_all_books_category_not_found(self):
        """Test that non-existent category returns empty list."""
        books = get_all_books("nonexistent")
        self.assertEqual(len(books), 0)

    def test_get_all_books_category_case_insensitive(self):
        """Test that category filter is case-insensitive."""
        books_upper = get_all_books("SELF-HELP")
        books_lower = get_all_books("self-help")
        books_mixed = get_all_books("SeLf-HeLp")
        self.assertEqual(len(books_upper), len(books_lower))
        self.assertEqual(len(books_lower), len(books_mixed))

    def test_get_book_by_title_found(self):
        """Test finding book by exact title."""
        book = get_book_by_title("Atomic Habits")
        self.assertIsNotNone(book)
        self.assertEqual(book.id, 1)  # type: ignore[union-attr]

    def test_get_book_by_title_case_insensitive(self):
        """Test that title search is case-insensitive."""
        book = get_book_by_title("atomic habits")
        self.assertIsNotNone(book)
        self.assertEqual(book.id, 1)  # type: ignore[union-attr]

    def test_get_book_by_title_not_found(self):
        """Test that non-existent title returns None."""
        book = get_book_by_title("Nonexistent Book")
        self.assertIsNone(book)

    def test_get_book_by_id_found(self):
        """Test finding book by ID."""
        book = get_book_by_id(1)
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Atomic Habits")  # type: ignore[union-attr]

    def test_get_book_by_id_not_found(self):
        """Test that non-existent ID returns None."""
        book = get_book_by_id(9999)
        self.assertIsNone(book)

    def test_create_book(self):
        """Test creating a new book."""
        initial_count = len(BOOKS)
        new_book = Book(
            id=200,
            title="New Book",
            author="New Author",
            category="New Category",
        )
        result = create_book(new_book)
        self.assertEqual(len(BOOKS), initial_count + 1)
        self.assertEqual(result.id, 200)

    def test_update_book_success(self):
        """Test successfully updating a book."""
        new_book = Book(
            id=1,
            title="Updated Title",
            author="Updated Author",
            category="Updated Category",
        )
        result = update_book(1, new_book)
        self.assertTrue(result)
        updated = get_book_by_id(1)
        self.assertEqual(updated.title, "Updated Title")  # type: ignore[union-attr]

    def test_update_book_not_found(self):
        """Test updating non-existent book returns False."""
        new_book = Book(
            id=999,
            title="Updated Title",
            author="Updated Author",
            category="Updated Category",
        )
        result = update_book(999, new_book)
        self.assertFalse(result)

    def test_delete_book_success(self):
        """Test successfully deleting a book."""
        initial_count = len(BOOKS)
        result = delete_book(1)
        self.assertTrue(result)
        self.assertEqual(len(BOOKS), initial_count - 1)
        self.assertIsNone(get_book_by_id(1))

    def test_delete_book_not_found(self):
        """Test deleting non-existent book returns False."""
        result = delete_book(9999)
        self.assertFalse(result)

    def test_reset_books(self):
        """Test that reset_books restores initial state."""
        create_book(
            Book(
                id=200,
                title="Test",
                author="Test",
                category="Test",
            )
        )
        self.assertEqual(len(BOOKS), 6)
        reset_books()
        self.assertEqual(len(BOOKS), 5)


if __name__ == "__main__":
    unittest.main()
