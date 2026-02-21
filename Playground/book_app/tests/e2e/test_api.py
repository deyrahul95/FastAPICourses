import unittest
from fastapi.testclient import TestClient

from app import create_app
from app.db import reset_books


class TestBooksAPI(unittest.TestCase):
    """E2E tests for all book API endpoints."""

    def setUp(self):
        """Initialize test client and reset database before each test."""
        self.app = create_app()
        self.client = TestClient(self.app)
        reset_books()

    def tearDown(self):
        """Reset database after each test."""
        reset_books()

    def test_get_all_books_success(self):
        """Test GET /api/books returns all books."""
        response = self.client.get("/api/books")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 50)
        self.assertEqual(data[0]["title"], "Atomic Habits")

    def test_get_all_books_with_category_filter(self):
        """Test GET /api/books?category=<category> filters results."""
        response = self.client.get("/api/books?category=Self-Help")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 10)
        for book in data:
            self.assertEqual(book["category"], "Self-Help")

    def test_get_all_books_category_case_insensitive(self):
        """Test that category filter is case-insensitive."""
        response = self.client.get("/api/books?category=self-help")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 10)

    def test_get_all_books_category_not_found(self):
        """Test GET /api/books with non-existent category."""
        response = self.client.get("/api/books?category=nonexistent")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_book_by_title_success(self):
        """Test GET /api/books/{title} returns correct book."""
        response = self.client.get("/api/books/Atomic Habits")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Atomic Habits")

    def test_get_book_by_title_case_insensitive(self):
        """Test that title search is case-insensitive."""
        response = self.client.get("/api/books/atomic habits")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    def test_get_book_by_title_not_found(self):
        """Test GET /api/books/{title} returns 404 for non-existent book."""
        response = self.client.get("/api/books/Nonexistent Book Title")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_get_book_by_id_success(self):
        """Test GET /api/books/{id}/details returns correct book."""
        response = self.client.get("/api/books/1/details")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], "Atomic Habits")

    def test_get_book_by_id_not_found(self):
        """Test GET /api/books/{id}/details returns 404 for non-existent ID."""
        response = self.client.get("/api/books/999/details")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_create_book_success(self):
        """Test POST /api/books creates new book."""
        payload = {
            "title": "New Test Book",
            "author": "Test Author",
            "category": "Testing",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "New Test Book")
        self.assertEqual(data["author"], "Test Author")
        self.assertEqual(data["category"], "Testing")
        self.assertIn("id", data)
        self.assertIn("updated_at", data)

    def test_create_book_title_too_short(self):
        """Test POST /api/books with title < 5 chars returns 422."""
        payload = {
            "title": "abc",
            "author": "Author",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_title_too_long(self):
        """Test POST /api/books with title > 100 chars returns 422."""
        payload = {
            "title": "x" * 101,
            "author": "Author",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_author_too_short(self):
        """Test POST /api/books with author < 2 chars returns 422."""
        payload = {
            "title": "Valid Title",
            "author": "A",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_category_too_short(self):
        """Test POST /api/books with category < 3 chars returns 422."""
        payload = {
            "title": "Valid Title",
            "author": "Author",
            "category": "ab",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_missing_title(self):
        """Test POST /api/books with missing title returns 422."""
        payload = {
            "author": "Author",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_missing_author(self):
        """Test POST /api/books with missing author returns 422."""
        payload = {
            "title": "Valid Title",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_create_book_missing_category(self):
        """Test POST /api/books with missing category returns 422."""
        payload = {
            "title": "Valid Title",
            "author": "Author",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_update_book_success(self):
        """Test PUT /api/books/{id} updates book."""
        payload = {
            "title": "Updated Title",
            "author": "Updated Author",
            "category": "Updated Category",
        }
        response = self.client.put("/api/books/1", json=payload)
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get("/api/books/1/details")
        data = get_response.json()
        self.assertEqual(data["title"], "Updated Title")
        self.assertEqual(data["author"], "Updated Author")
        self.assertEqual(data["category"], "Updated Category")

    def test_update_book_partial(self):
        """Test PUT /api/books/{id} with partial update."""
        payload = {"title": "Partial Update"}
        response = self.client.put("/api/books/1", json=payload)
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get("/api/books/1/details")
        data = get_response.json()
        self.assertEqual(data["title"], "Partial Update")
        self.assertEqual(data["author"], "James Clear")

    def test_update_book_not_found(self):
        """Test PUT /api/books/{id} returns 404 for non-existent book."""
        payload = {"title": "Updated Title"}
        response = self.client.put("/api/books/999", json=payload)
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_update_book_validation_error(self):
        """Test PUT /api/books/{id} with invalid data returns 422."""
        payload = {"title": "ab"}
        response = self.client.put("/api/books/1", json=payload)
        self.assertEqual(response.status_code, 422)

    def test_delete_book_success(self):
        """Test DELETE /api/books/{id} deletes book."""
        response = self.client.delete("/api/books/1")
        self.assertEqual(response.status_code, 204)

        get_response = self.client.get("/api/books/1/details")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_book_not_found(self):
        """Test DELETE /api/books/{id} returns 404 for non-existent book."""
        response = self.client.delete("/api/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_route_ordering_details_before_title(self):
        """Test that /api/books/1/details works (not treated as title)."""
        response = self.client.get("/api/books/1/details")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], 1)

    def test_special_characters_in_title(self):
        """Test handling of special characters in book title."""
        payload = {
            "title": "Book with Special Chars: !@#$%^&*()",
            "author": "Test Author",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_unicode_in_title(self):
        """Test handling of unicode characters in book title."""
        payload = {
            "title": "Unicode Book Title: 日本語",
            "author": "Test Author",
            "category": "Test",
        }
        response = self.client.post("/api/books", json=payload)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
