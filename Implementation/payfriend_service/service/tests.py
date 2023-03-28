from django.test import TestCase
from datetime import *

# Context Imports
from .classes.contexts.users.users_context import UsersContext
from .classes.contexts.transactions.transactions_context import TransactionsContext

# Component Imports
from .classes.component.auth.auth import AuthComponent
from .classes.component.pay.pay import PaymentComponent

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


class AuthComponentTestCase(TestCase):

    def setUp(self):
        self.auth_component = AuthComponent()
        # Different account types to test component functionality and validation flows
        self.valid_account = {
            "email": "abcdef@hotmail.com",
            "password": "pass12345678"
        }
        self.invalid_account_1 = {
            "email": "abcdef@hotmail.com",
            "password": ""
        }
        self.invalid_account_2 = {
            "email": "abcdef@...com",
            "password": "pass12345678"
        }
    
    def test_register_user(self):
        """
        User is correctly registered on the service
        """
        # Arrange
        status_1 = self.auth_component.register_user(self.valid_account["email"], self.valid_account["password"])
        status_2 = self.auth_component.register_user(self.invalid_account_1["email"], self.invalid_account_1["password"])
        status_3 = self.auth_component.register_user(self.invalid_account_2["email"], self.invalid_account_2["password"])
        # Assert
        self.assertEqual(status_1, 0, "Valid account should be successfully registered on service.")
        self.assertEqual(status_2, -3, "Invalid account (weak or no password) should not be registered on service.")
        self.assertEqual(status_3, -2, "Invalid account (invalid email) should not be registered on service.")

    def test_authenticate_user(self):
        """
        User is correctly authenticated or restricted on the service
        """
        # Arrange
        self.auth_component.register_user(self.valid_account["email"], self.valid_account["password"])
        registered = self.auth_component.authenticate_user(self.valid_account["email"], self.valid_account["password"])
        registered_forbidden = self.auth_component.authenticate_user(self.valid_account["email"], "pass1234567899Wrong")
        # Assert
        self.assertEqual(registered, 0, "Valid account should be successfully authenticated on service.")
        self.assertEqual(registered_forbidden, -1, "Invalid credentials should not authenticate on service.")


class PaymentComponentTestCase(TestCase):

    def setUp(self):
        self.transactions_context = TransactionsContext()
        self.auth_component = AuthComponent()
        self.payment_component = PaymentComponent()
        # Setup account to use for transactions
        self.valid_account = {
            "email": "abcdef@hotmail.com",
            "password": "pass12345678"
        }
        self.auth_component.register_user(self.valid_account["email"], self.valid_account["password"])

    def test_process_payment(self):
        # Setup
        email = self.valid_account["email"]
        password = self.valid_account["password"]
        transaction_1, err_1 = self.payment_component.process_payment(email, \
            password, 10.05, "TEST") # valid
        transaction_2, err_2 = self.payment_component.process_payment(email, \
            password, -10.05, "TEST") # invalid - value
        transaction_3, err_3 = self.payment_component.process_payment(email, \
            password, 10.05, "") # invalid - company
        transaction_4, err_4 = self.payment_component.process_payment(email, \
            password + "xxx", 10.05, "TEST") # invalid - account
        # Assert
        # T1
        self.assertIsNone(err_1, "Transaction 1 should be processed successfully")
        self.assertIsNotNone(transaction_1, "Transaction 1 should return a transaction obj")
        # T2
        self.assertIsNone(transaction_2, "Transaction 2 should not be processed")
        self.assertIsNotNone(err_2, "Transaction 2 should return an error")
        self.assertEqual(err_2, "Payment details not valid (Transaction value).", "Transaction 2 should return the correct error message")
        # T3
        self.assertIsNone(transaction_3, "Transaction 3 should not be processed")
        self.assertIsNotNone(err_3, "Transaction 3 should return an error")
        self.assertEqual(err_3, "Payment details not valid (Company name).", "Transaction 3 should return the correct error message")
        # T4
        self.assertIsNone(transaction_4, "Transaction 4 should not be processed")
        self.assertIsNotNone(err_4, "Transaction 4 should return an error")
        self.assertEqual(err_4, f"Provided account credentials are incorrect.", "Transaction 4 should return the correct error message")

    def test_delete_payment(self):
        # Setup
        email = self.valid_account["email"]
        password = self.valid_account["password"]
        transaction_1, err_1 = self.payment_component.process_payment(email, \
            password, 10.05, "TEST")
        id = transaction_1["id"]
        deleted = self.payment_component.delete_payment(id)
        t, err = self.transactions_context.get_transaction_from_table(id)
        # Assert
        self.assertEqual(deleted, True, f"Transaction with ID {id} should be deleted successfully")
        self.assertIsNone(t, f"Transaction with ID {id} should return a transaction obj")
        self.assertEqual(err, f"Transaction wth ID {id} not found in DB.", f"The DB should not have any record of transaction wth ID {id}")
    