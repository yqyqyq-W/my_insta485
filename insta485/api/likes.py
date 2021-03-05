"""REST API for likes."""
import flask
import insta485
from flask import request, session, jsonify


"""exception class"""


# class InvalidUsage(Exception):
#     status_code = 400
#
#     def __init__(self, message, status_code=None, payload=None):
#         Exception.__init__(self)
#         self.message = message
#         if status_code is not None:
#             self.status_code = status_code
#         self.payload = payload
#
#     def to_dict(self):
#         rv = dict(self.payload or ())
#         rv['message'] = self.message
#         return rv
#
#
# @insta485.app.errorhandler(InvalidUsage)
# def handle_invalid_usage(error):
#     response = jsonify(error.to_dict())
#     response.status_code = error.status_code
#     return response
#
#
# @insta485.app.before_request
# def is_login():
#     """Check login."""
#     if 'username' not in session:
#         if request.endpoint in ['get_likes', 'delete_likes', 'post_likes']:
#             raise InvalidUsage('Forbidden', status_code=403)
#     return None


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["GET"])
def get_likes(postid_url_slug):
    counter = 0
    iflike = 0
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT *"
        " FROM likes"
        " WHERE postid = ?", (postid_url_slug,)
    )
    like_list = cur.fetchall()
    for like in like_list:
        counter = counter + 1
        if like['owner'] == session['username']:
            iflike = 1
    context = {
        "logname_likes_this": iflike,
        "likes_count": counter,
        "postid": postid_url_slug,
        "url": flask.request.path,
    }
    return jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["DELETE"])
def delete_likes(postid_url_slug):
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT *"
        " FROM likes"
        " WHERE postid = ? AND owner = ?", (str(postid_url_slug), session['username'])
    )
    like_list = cur.fetchall()
    if not bool(like_list):
        cur = connection.execute(
            "DELETE"
            " FROM likes"
            " WHERE postid = ? AND owner = ?", (str(postid_url_slug), session['username'])
        )
    return '', 204


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["POST"])
def post_likes(postid_url_slug):
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT *"
        " FROM likes"
        " WHERE postid = ? AND owner = ?", (str(postid_url_slug), session['username'])
    )
    like_list = cur.fetchall()
    if bool(like_list):
        connection.execute(
            "INSERT INTO likes(owner, postid)"
            " VALUES (?, ?)", (session['username'], str(postid_url_slug))
        )
        context = {
            "logname": session['username'],
            "postid": postid_url_slug,
        }
        return jsonify(**context), 'CREATED', 201
    else:
        context = {
            "logname": session['username'],
            "message": "Conflict",
            "postid": postid_url_slug,
            "status_code": 409,
        }
        return jsonify(**context), 'CONFLICT', 409
