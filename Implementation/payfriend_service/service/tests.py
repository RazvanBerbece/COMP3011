from django.test import TestCase

# Model Imports
from .models import Transaction

# Context Imports
from .classes.contexts.users.users_context import UsersContext
from .classes.contexts.transactions.transactions_context import TransactionsContext

# Create your tests here.

class UserContextTestCase(TestCase):

    def setUp(self):
        self.users_context = UsersContext()
        # Setup test user accounts
        self.valid_account = {
            "email": "abc@test.com",
            "hash": "d0fd5133c6ac19aaf89def3d8ae6e9c30b5ea0bb2ca6091d2265d83426761103",
            "salt": "8e32f30bb98d0f1d"
        }
        self.users_context.add_user_to_table(self.valid_account["email"], \
            self.valid_account["hash"], self.valid_account["salt"])
    
    def test_add_user_to_table(self):
        """
        User is correctly added and found in sqlite3 Users table
        """
        email = self.valid_account["email"]
        exists = self.users_context.email_exists(email)
        self.assertEqual(exists, True, f"Account {email} not found in Users table.")
    
    def test_get_salt_for_email(self):
        """
        Salt is correctly retrieved for email from sqlite3 Users table
        """
        email = self.valid_account["email"]
        expected_salt = self.valid_account["salt"]
        actual_salt = self.users_context.get_salt_for_email(email)
        self.assertEqual(expected_salt, actual_salt, f"Expected salt and actual salt do not match.")
    
    def test_user_is_registered(self):
        """
        User is correctly retrieved from Users table using email and hash
        """
        email = self.valid_account["email"]
        hash = self.valid_account["hash"]
        registered = self.users_context.user_is_registered(email, hash)
        self.assertEqual(registered, True, f"Test account should be in Users table.")

class TransactionContextTestCase(TestCase):

    def setUp(self):
        self.transactions_context = TransactionsContext()
        # Setup VALID transaction objects
        self.valid_transaction = {
            "id": "id123",
            "email": "abc@test.com",
            "value": 10.666,
            "timestamp": 170000.560,
            "company": "TestFlights"
        }
        self.valid_transaction_to_delete = {
            "id": "id1234",
            "email": "abc@test.com",
            "value": 10.666,
            "timestamp": 170000.560,
            "company": "TestFlights"
        }
        self.transactions_context.add_transaction_to_table(self.valid_transaction)
        self.transactions_context.add_transaction_to_table(self.valid_transaction_to_delete)
    
    def test_add_transaction_to_table(self):
        """
        Transaction is correctly added and found in sqlite3 Transactions table
        """
        ### Happy path - Transaction exists
        actual_transaction, err = self.transactions_context.get_transaction_from_table(self.valid_transaction["id"])
        self.assertIsNotNone(actual_transaction, f"Transaction with ID id123 should be in the Transactions table.")
        ### Sad path - Transaction does not exist
        unexisting_transaction, err = self.transactions_context.get_transaction_from_table("idWhichDoesNotExist")
        self.assertIsNone(unexisting_transaction, f"Transaction with ID id123 shouldn't be in the Transactions table.")
    
    def test_delete_transaction_from_table(self):
        """
        Transaction is correctly removed and then not found in sqlite3 Transactions table
        """
        ### Happy path - Transaction exists and gets deleted
        status, err = self.transactions_context.delete_transaction_from_table(self.valid_transaction_to_delete["id"])
        self.assertEqual(status, 0, f"Transaction with ID id1234 should be deleted from the Transactions table.")
        t, err = self.transactions_context.get_transaction_from_table("id1234")
        self.assertIsNone(t, f"Transaction with ID id1234 shouldn't be in the Transactions table.")
        ### Sad path - Transaction does not exist and try to delete
        status_sad_path, err = self.transactions_context.delete_transaction_from_table("idWhichDoesNotExist")
        self.assertEqual(status_sad_path, -1, f"Transaction with ID idWhichDoesNotExist shouldn't be in the Transactions table to be deleted.")