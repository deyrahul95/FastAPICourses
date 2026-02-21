import unittest
from datetime import datetime
from pydantic import ValidationError

from app.models import Book, AddBookDto, UpdateBookDto


class TestBookModel(unittest.TestCase):
    """Unit tests for the Book model."""

    def test_book_creation(self):
        """Test creating a Book instance with all required fields."""
        book = Book(
            id=1,
            title="Test Book",
            author="Test Author",
            category="Test Category",
        )
        self.assertEqual(book.id, 1)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.category, "Test Category")
        self.assertIsNotNone(book.updated_at)

    def test_book_has_updated_at(self):
        """Test that Book has updated_at field with default."""
        book = Book(
            id=1,
            title="Test Book",
            author="Test Author",
            category="Test",
        )
        self.assertIsInstance(book.updated_at, datetime)

    def test_book_with_custom_updated_at(self):
        """Test creating Book with custom updated_at value."""
        custom_time = datetime(2024, 1, 1, 12, 0, 0)
        book = Book(
            id=1,
            title="Test Book",
            author="Test Author",
            category="Test",
            updated_at=custom_time,
        )
        self.assertEqual(book.updated_at, custom_time)


class TestAddBookDtoModel(unittest.TestCase):
    """Unit tests for the AddBookDto model."""

    def test_add_book_dto_valid(self):
        """Test creating AddBookDto with valid data."""
        dto = AddBookDto(
            title="Valid Book Title",
            author="Author",
            category="Test",
        )
        self.assertEqual(dto.title, "Valid Book Title")
        self.assertEqual(dto.author, "Author")
        self.assertEqual(dto.category, "Test")

    def test_add_book_dto_title_too_short(self):
        """Test that title below min_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="abc", author="Author", category="Test")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("title",) for e in errors))

    def test_add_book_dto_title_too_long(self):
        """Test that title above max_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="x" * 101, author="Author", category="Test")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("title",) for e in errors))

    def test_add_book_dto_author_too_short(self):
        """Test that author below min_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="Valid Title", author="A", category="Test")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("author",) for e in errors))

    def test_add_book_dto_author_too_long(self):
        """Test that author above max_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="Valid Title", author="x" * 51, category="Test")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("author",) for e in errors))

    def test_add_book_dto_category_too_short(self):
        """Test that category below min_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="Valid Title", author="Author", category="ab")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("category",) for e in errors))

    def test_add_book_dto_category_too_long(self):
        """Test that category above max_length raises ValidationError."""
        with self.assertRaises(ValidationError) as ctx:
            AddBookDto(title="Valid Title", author="Author", category="x" * 21)
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("category",) for e in errors))

    def test_add_book_dto_title_required(self):
        """Test that missing title raises ValidationError."""
        with self.assertRaises(ValidationError):
            AddBookDto(author="Author", category="Test")  # type: ignore[call-arg]

    def test_add_book_dto_author_required(self):
        """Test that missing author raises ValidationError."""
        with self.assertRaises(ValidationError):
            AddBookDto(title="Valid Title", category="Test")  # type: ignore[call-arg]

    def test_add_book_dto_category_required(self):
        """Test that missing category raises ValidationError."""
        with self.assertRaises(ValidationError):
            AddBookDto(title="Valid Title", author="Author")  # type: ignore[call-arg]


class TestUpdateBookDtoModel(unittest.TestCase):
    """Unit tests for the UpdateBookDto model."""

    def test_update_book_dto_all_fields(self):
        """Test UpdateBookDto with all fields provided."""
        dto = UpdateBookDto(
            title="New Title",
            author="New Author",
            category="New Category",
        )
        self.assertEqual(dto.title, "New Title")
        self.assertEqual(dto.author, "New Author")
        self.assertEqual(dto.category, "New Category")

    def test_update_book_dto_partial_update(self):
        """Test UpdateBookDto with only title provided."""
        dto = UpdateBookDto(title="New Title")
        self.assertEqual(dto.title, "New Title")
        self.assertIsNone(dto.author)
        self.assertIsNone(dto.category)

    def test_update_book_dto_empty(self):
        """Test UpdateBookDto with no fields (all optional)."""
        dto = UpdateBookDto()
        self.assertIsNone(dto.title)
        self.assertIsNone(dto.author)
        self.assertIsNone(dto.category)

    def test_update_book_dto_title_validation(self):
        """Test that title validation still applies for updates."""
        with self.assertRaises(ValidationError) as ctx:
            UpdateBookDto(title="abc")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("title",) for e in errors))

    def test_update_book_dto_author_validation(self):
        """Test that author validation still applies for updates."""
        with self.assertRaises(ValidationError) as ctx:
            UpdateBookDto(author="A")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("author",) for e in errors))

    def test_update_book_dto_category_validation(self):
        """Test that category validation still applies for updates."""
        with self.assertRaises(ValidationError) as ctx:
            UpdateBookDto(category="ab")
        errors = ctx.exception.errors()
        self.assertTrue(any(e["loc"] == ("category",) for e in errors))


if __name__ == "__main__":
    unittest.main()
