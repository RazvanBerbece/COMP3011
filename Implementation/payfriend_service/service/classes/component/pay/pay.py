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

    def process_payment(self, email: str, password: str, value: float, company: str):
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
        # Process payment
        transaction = {
            "id": str(uuid.uuid4()),
            "value": value,
            "email": email,
            "timestamp": datetime.now(timezone.utc).timestamp() * 1000, # in milliseconds since Unix epoch
            "company": company
        }
        # Store transaction
        self.transactions_context.add_transaction_to_table(transaction)
        return transaction, None

    def delete_payment(self, transactionId: str):
        # Input validation
        if (transactionId == ""):
            return False
        status = self.transactions_context.delete_transaction_from_table(transactionId)
        if (status == -1):
            return False
        return True