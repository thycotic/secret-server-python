class ApiError(Exception):
    def __init__(self, message, response):
        super(ApiError, self).__init__(message)
        self.message = message
        self.response = {
            "statusCode" : response.status_code,
            "body" : response.json()["message"]
        }
        return
    def __str__(self):
        return repr(self.message, self.response)

class HandleApiResponse():
    def __init__(self, response):
        if response.status_code is not 200 and response.status_code is not 204:
            if response.json() and response.json()["errorCode"] and len(response.json()["errorCode"]) > 0:
                message = response.json()["errorCode"]
            else:
                message = "Status: {code}".format(code=response.status_code)
            raise ApiError(message, response)
        self.response = response.json()
        