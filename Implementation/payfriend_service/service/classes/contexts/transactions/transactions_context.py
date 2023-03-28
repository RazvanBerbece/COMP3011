from ....models import Transaction

class TransactionsContext:
    """
    DB Context interface.
    Manages connecting to the sqlite3 DB and querying the Transactions table
    """

    @staticmethod
    def add_transaction_to_table(transaction: object):
        transaction = Transaction(TransactionId=transaction["id"], \
             Value=transaction["value"], \
             CustomerEmail=transaction["email"], \
             Timestamp=transaction["timestamp"], \
             Company=transaction["company"])
        transaction.save()
    
    @staticmethod
    def delete_transaction_from_table(transactionId: str):
        pass

