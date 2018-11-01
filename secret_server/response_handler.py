class ApiError(Exception):
    def __init__(self, message, response):
        super(ApiError, self).__init__(message)
        self.message = message
        self.response = {
            "Error Code": self.message,
            "statusCode": response.status_code,
            "Message": response.json()["message"]
        }

    def __str__(self):
        return repr(self.response)


def api_response(response):
    if response.status_code is not 200 and response.status_code is not 204:
        if 'errorCode' in response.json():
            if response.json() and response.json()["errorCode"] and len(response.json()["errorCode"]) > 0:
                message = response.json()["errorCode"]
            else:
                message = "Status: {code}".format(code=response.status_code)
        else:
            message = response.json()
        raise ApiError(message, response)
    response.close()
    return response.json()
