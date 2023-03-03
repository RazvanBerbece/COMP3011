import json

# Response model returned by service
class Response:

    def __init__(self, statusCode: int, resource: str, message: str, data: object, timestamp: str):
        self.statusCode = statusCode    # status code of operation (200 success, 400 client error, 500 server error)
        self.resource = resource        # resource path which was accessed
        self.message = message          # human readable message describing result / error of operation
        self.data = data                # object (usually a dictionary) which holds data returned by service (if needed)
        self.timestamp = timestamp      # UTC.Now timestamp when response was sent by service
    
    def get_json_string(self):
        return json.dumps(self.__dict__)