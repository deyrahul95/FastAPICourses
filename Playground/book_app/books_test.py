from typing import List
import unittest
import threading
from fastapi.testclient import TestClient
from books import app


class TestConcurrency(unittest.TestCase):
    def setUp(self) -> None:
        self.client: TestClient = TestClient(app)

    def test_concurrent_requests(self) -> None:
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

        # Create 10 threads to send concurrent requests
        for i in range(10):
            thread: threading.Thread = threading.Thread(
                target=send_request, args=(results, i)
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Assert to check if unique book IDs were created correctly
        unique_ids = set(results)
        self.assertEqual(
            len(unique_ids),
            len(results),
            "Race condition occurred or duplicate IDs detected.",
        )
        self.assertEqual(
            max(results),
            min(results) + len(results) - 1,
            "book_id increments are not correct.",
        )


if __name__ == "__main__":
    unittest.main()
