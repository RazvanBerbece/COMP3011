class PaymentResponse:
    """
    Response structure returned by service on the `/pay` endpoint
    """

    def __init__(self, transactionId: str, error: object, timestamp: str):
        self._resource = "/pay"               # resource path which was accessed
        self._error = error                   # dictionary holding details about error if occured / null
        self._timestamp = timestamp           # UTC.Now timestamp when payment was processed by service
        self.transactionId = transactionId    # GUID generated in case of a successful payment
    
    def get_json(self):
        return {
            "_resource": self._resource,
            "_timestamp": self._timestamp,
            "_error": self._error,
            "transactionId": self.transactionId,
        }