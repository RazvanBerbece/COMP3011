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
             Company=transaction["company"],
             City=transaction["city"], \
             Postcode=transaction["postcode"], \
             Country=transaction["country"], \
             SourceCurrency=transaction["currency"], \
             SysCurrency="GBP", \
        )
        transaction.save()
    
    @staticmethod
    def get_transaction_from_table(transactionId: str):
        try:
            t = Transaction.objects.get(TransactionId=transactionId)
            return {
                "id": f"{t.TransactionId}",
                "email": f"{t.CustomerEmail}",
                "value": t.Value,
                "timestamp": t.Timestamp,
                "company": f"{t.Company}",
                "city": f"{t.City}",
                "postcode": f"{t.Postcode}",
                "country": f"{t.Country}",
                "sourceCurrency": f"{t.SourceCurrency}",
                "sysCurrency": f"{t.SysCurrency}"
            }, None
        except:
            return None, f"Transaction wth ID {transactionId} not found in DB."
    
    @staticmethod
    def delete_transaction_from_table(transactionId: str):
        try:
            t = Transaction.objects.get(TransactionId=transactionId)
            t.delete()
            return 0, None
        except:
            return -1, f"Transaction wth ID {transactionId} not found in DB."

