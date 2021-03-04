"""REST API for error handling."""
import flask
import insta485
from flask import request, session, jsonify


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@insta485.app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@insta485.app.before_request
def is_login():
    """Check login."""
    if 'username' not in session:
        if request.endpoint in ['get_likes', 'delete_likes', 'post_likes', 'get_post', 'get_comments', 'post_comments']:
            raise InvalidUsage('Forbidden', status_code=403)
    return None
