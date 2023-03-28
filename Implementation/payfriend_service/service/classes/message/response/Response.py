import json

class Response:
    """
    Response structure returned by service on the `/signup`, `DELETE /{transactionId}` endpoints.
    Can be used for more general endpoints as well.
    """

    def __init__(self, resource: str, transactionId: str, error: object, timestamp: str, success: int):
        self._resource = resource           # resource path which was accessed
        self._error = error                 # dictionary holding details about error if occured / null
        self._timestamp = timestamp         # UTC.Now timestamp when payment was processed by service
        self.transactionId = transactionId  # GUID generated in case of a successful payment
        self.success = success              # Whether operation succeeded
    
    def get_json_string(self):
        return json.dumps(self.__dict__)