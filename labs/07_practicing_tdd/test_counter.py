"""
Test Cases for Counter Web Service
"""
from unittest import TestCase
import status
from counter import app

class CounterTest(TestCase):
    """Test Cases for Counter Web Service"""

    def setUp(self):
        self.client = app.test_client()  

    def test_create_a_counter(self):
        """It should create a counter"""
        result = self.client.post("/counters/foo")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        data = result.get_json()
        self.assertIn("foo", data)
        self.assertEqual(data["foo"], 0)

    def test_duplicate_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post("/counters/bar")
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It shoud increment existing counter"""
        result = self.client.post("/counters/counter_1")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        baseline = result.get_json()["counter_1"]
        result = self.client.put("/counters/counter_1")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        data = result.get_json()
        self.assertEqual(data["counter_1"], baseline+1)

    def test_update_a_counter_faled(self):
        """It shoud return 404 error"""
        result = self.client.put("/counters/not_existing_counter")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_a_counter(self):
        """It shoud return existing counter"""
        result = self.client.post("/counters/counter_3")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get("/counters/counter_3")
        data = result.get_json()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(data["counter_3"], 0)

    def test_read_a_counter_faled(self):
        """It shoud return 404 error"""
        result = self.client.get("/counters/not_existing_counter")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter(self):
        """It shoud delete existing counter"""
        result = self.client.post("/counters/counter_4")
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.get("/counters/counter_4")
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        result = self.client.delete("/counters/counter_4")
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        result = self.client.get("/counters/counter_4")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_a_counter_faled(self):
        """It shoud return 404 error"""
        result = self.client.delete("/counters/not_existing_counter")
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)

