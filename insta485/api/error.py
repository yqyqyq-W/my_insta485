"""REST API for error handling."""
from flask import jsonify
import insta485


class InvalidUsage(Exception):
    """Invalid usage."""

    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        """Init."""
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """To dict."""
        response = dict(self.payload or ())
        response['message'] = self.message
        response['status_code'] = self.status_code
        return response


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    """Handle invalid."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
