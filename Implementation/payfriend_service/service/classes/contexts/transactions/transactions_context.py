from ....models import Transaction

class TransactionsContext:
    """
    DB Context interface.
    Manages connecting to the sqlite3 DB and querying the Transactions table
    """

    @staticmethod
    def add_transaction_to_table():
        pass
    
    @staticmethod
    def delete_transaction_from_table():
        pass

