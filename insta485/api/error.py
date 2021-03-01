"""REST API for error handling."""
import flask
import insta485
from flask import request, session, jsonify


@insta485.errorhandler(Exception)
def handle_invalid_usage(error, code):
    response = {"message": error, "status_code": code}
    return jsonify(**response)


@insta485.app.before_request
def is_login():
    """Get&before request."""
    if 'username' not in session:
        if request.endpoint in ['get_post', 'get_comments', 'post_comments']:
            raise Exception("Forbidden", 403)
