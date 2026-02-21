from typing import List
import unittest
import threading

from fastapi.testclient import TestClient
from app import create_app
from app.db import reset_books


class TestConcurrency(unittest.TestCase):
    """Test suite for concurrent request handling."""

    def setUp(self) -> None:
        """Initialize test client before each test."""
        self.app = create_app()
        self.client: TestClient = TestClient(self.app)
        reset_books()

    def tearDown(self) -> None:
        """Clean up database after each test to prevent pollution."""
        reset_books()

    def test_concurrent_requests(self) -> None:
        """Test that concurrent POST requests generate unique, sequential IDs."""

        def send_request(results: List[int], index: int) -> None:
            response = self.client.post(
                "/books",
                json={
                    "title": "Test Book",
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


if __name__ == "__main__":
    unittest.main()
