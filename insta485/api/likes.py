"""REST API for likes."""
import flask
from flask import session, jsonify
import insta485
from insta485.api.error import InvalidUsage
from insta485.api.comments import check_postid


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/', methods=["GET"])
def get_likes(postid_url_slug):
    """Get likes."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid_url_slug)
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


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["DELETE"])
def delete_likes(postid_url_slug):
    """Delete likes."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid_url_slug)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT *"
        " FROM likes"
        " WHERE postid = ? AND owner = ?",
        (postid_url_slug, session['username'])
    )
    like_list = cur.fetchall()
    if bool(like_list):
        cur = connection.execute(
            "DELETE"
            " FROM likes"
            " WHERE postid = ? AND owner = ?",
            (postid_url_slug, session['username'])
        )
    return '', 204


@insta485.app.route('/api/v1/p/<int:postid_url_slug>/likes/',
                    methods=["POST"])
def post_likes(postid_url_slug):
    """Post likes."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid_url_slug)
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT *"
        " FROM likes"
        " WHERE postid = ? AND owner = ?",
        (postid_url_slug, session['username'])
    )
    like_list = cur.fetchall()

    if not bool(like_list):
        connection.execute(
            "INSERT INTO likes(owner, postid)"
            " VALUES (?, ?)", (session['username'], postid_url_slug)
        )
        context = {
            "logname": session['username'],
            "postid": postid_url_slug,
        }
        status_code = 201
    else:
        context = {
            "logname": session['username'],
            "message": "Conflict",
            "postid": postid_url_slug,
            "status_code": 409,
        }
        status_code = 409

    return jsonify(**context), status_code
