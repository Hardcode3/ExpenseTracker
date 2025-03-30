import unittest
import uuid
import requests

API_URL = "http://localhost:8000/transaction"

class TestTransactionRoutesDocker(unittest.TestCase):

    def setUp(self):
        self.transaction_id = None

    def test_create_transaction_success(self):
        transaction_data = {
            "amount": 100.0,
            "method": "credit_card",
            "date": "2025-03-30T12:00:00",
            "description": "Test transaction"
        }
        response = requests.post(f"{API_URL}/", json=transaction_data)
        self.assertEqual(response.status_code, 201)
        self.transaction_id = response.json()["id"]

    def test_get_all_transactions(self):
        response = requests.get(API_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    def test_get_single_transaction_not_found(self):
        random_id = uuid.uuid4()
        response = requests.get(f"{API_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)

    def test_get_single_transaction_success(self):
        transaction_data = {
            "amount": 50.0,
            "method": "debit_card",
            "date": "2025-03-30T14:00:00",
            "description": "Another transaction"
        }
        create_response = requests.post(f"{API_URL}/", json=transaction_data)
        transaction_id = create_response.json()["id"]

        response = requests.get(f"{API_URL}/{transaction_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], transaction_id)

    def test_delete_transaction_success(self):
        transaction_data = {
            "amount": 75.0,
            "method": "paypal",
            "date": "2025-03-30T16:00:00",
            "description": "Transaction to delete"
        }
        create_response = requests.post(f"{API_URL}/", json=transaction_data)
        transaction_id = create_response.json()["id"]

        response = requests.delete(f"{API_URL}/{transaction_id}")
        self.assertEqual(response.status_code, 204)

    def test_delete_transaction_not_found(self):
        random_id = uuid.uuid4()
        response = requests.delete(f"{API_URL}/{random_id}")
        self.assertEqual(response.status_code, 404)
