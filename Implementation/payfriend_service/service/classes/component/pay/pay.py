from ...contexts.transactions.transactions_context import *

class PaymentService():
    """
    Interface which provides methods for processing payments, generating transactions and deleting transactions
    and other utils
    """

    def __init__(self):
        self.transactions_context = TransactionsContext()