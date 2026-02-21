import unittest
from typing import List
import threading

from fastapi.testclient import TestClient

from app import create_app
from app.db import reset_books


class TestConcurrency(unittest.TestCase):
    """E2E tests for concurrent request handling."""

    def setUp(self):
        """Initialize test client and reset database before each test."""
        self.app = create_app()
        self.client = TestClient(self.app)
        reset_books()

    def tearDown(self):
        """Reset database after each test."""
        reset_books()

    def test_concurrent_create_requests(self):
        """Test that concurrent POST requests generate unique, sequential IDs."""

        def send_request(results: List[int], index: int) -> None:
            response = self.client.post(
                "/books",
                json={
                    "title": "Concurrent Test Book",
                    "author": "Test Author",
                    "category": "Test",
                },
            )
            results.append(response.json()["id"])

        results: List[int] = []
        threads: List[threading.Thread] = []

        for i in range(10):
            thread = threading.Thread(target=send_request, args=(results, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        unique_ids = set(results)
        self.assertEqual(
            len(unique_ids),
            len(results),
            "Race condition occurred - duplicate IDs detected",
        )
        self.assertEqual(
            max(results),
            min(results) + len(results) - 1,
            "Book ID increments are not sequential",
        )

    def test_concurrent_read_write(self):
        """Test concurrent read and write operations."""

        def read_books(results: List[int]) -> None:
            response = self.client.get("/books")
            results.append(len(response.json()))

        def write_book() -> None:
            self.client.post(
                "/books",
                json={
                    "title": "Concurrent Book",
                    "author": "Author",
                    "category": "Test",
                },
            )

        results: List[int] = []
        threads: List[threading.Thread] = []

        initial_count = 5

        for _ in range(5):
            thread = threading.Thread(target=read_books, args=(results,))
            threads.append(thread)
            thread.start()

        for _ in range(3):
            thread = threading.Thread(target=write_book)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        for count in results:
            self.assertLessEqual(count, initial_count + 3)


if __name__ == "__main__":
    unittest.main()
