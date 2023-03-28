import json

class PaymentResponse:
    """
    Response structure returned by service on the `/pay` endpoint
    """

    def __init__(self, transactionId: str, error: object, timestamp: str):
        self._resource = "/api/pay"           # resource path which was accessed
        self._error = error                   # dictionary holding details about error if occured / null
        self._timestamp = timestamp           # UTC.Now timestamp when payment was processed by service
        self.transactionId = transactionId    # GUID generated in case of a successful payment
    
    def get_json_string(self):
        return json.dumps(self.__dict__)