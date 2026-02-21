from typing import List
import unittest
import threading

from fastapi.testclient import TestClient
from app import create_app


class TestConcurrency(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.client: TestClient = TestClient(self.app)

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

        for i in range(10):
            thread: threading.Thread = threading.Thread(
                target=send_request, args=(results, i)
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

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
