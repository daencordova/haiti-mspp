from flask import make_response

from .status import HTTP_STATUS


class Response:
    @classmethod
    def get_message(cls, status, message, data=None):
        response = {"status": HTTP_STATUS[status], "message": message}

        if data or isinstance(data, list):
            response["data"] = data

        return make_response(response, status)

    @classmethod
    def get_error(cls, status, error):
        return make_response({"status": HTTP_STATUS[status], "error": error}, status)
