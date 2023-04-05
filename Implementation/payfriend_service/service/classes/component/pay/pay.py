import uuid
from datetime import *

from ...contexts.transactions.transactions_context import *
from ..auth.auth import AuthComponent

class PaymentComponent():
    """
    Interface which provides methods for processing payments, generating transactions and deleting transactions
    and other utils
    """

    def __init__(self):
        self.transactions_context = TransactionsContext()

    def process_payment(self, email: str, password: str, value: float, company: str, city: str, postcode: str, country: float, currency: str):
        """
        Processes a payment through the system, stores the record and returns a transaction object which holds the stores data,
        including the transaction ID.
        
        Returns a transaction object and error tuple, t being `None` if error occured, or err being `None` if the payment was processed
        """
        # Check that user is registered with the service
        auth = AuthComponent()
        registered = auth.authenticate_user(email, password)
        if (registered < 0):
            if registered == -1:
                return None, f"Provided account credentials are incorrect."
            elif registered == -2:
                return None, f"Provided email address is invalid."
            elif registered == -3:
                return None, f"Provided password is invalid."
        # Check that payment details are valid
        if (float(value) <= 0):
            return None, f"Payment details not valid (Transaction value)."
        if (company == ""):
            return None, f"Payment details not valid (Company name)."
        if (city == "" or postcode == "" or country == "" or currency == ""):
            return None, f"Billing details not valid (City, Postcode, Country, Currency)."
        # Process payment
        transaction = {
            "id": str(uuid.uuid4()),
            "value": value,
            "email": email,
            "timestamp": datetime.now(timezone.utc).timestamp() * 1000, # in milliseconds since Unix epoch
            "company": company,
            "city": city,
            "postcode": postcode,
            "country": country,
            "currency": currency
        }
        # Store transaction
        self.transactions_context.add_transaction_to_table(transaction)
        return transaction, None

    def delete_payment(self, transactionId: str):
        """
        Removes a transaction with the given `transactionId` from the store. 
        
        Returns:
        - `0` if transaction was deleted successfully.
        - `-2` if `transactionId` is not a valid string
        - `-1` if transaction with given id could not be found in store
        """
        # Input validation
        if (transactionId == ""):
            return -2
        status = self.transactions_context.delete_transaction_from_table(transactionId)
        if (status[0] == -1):
            return -1
        return 0