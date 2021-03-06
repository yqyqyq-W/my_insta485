"""REST API for comments."""
import flask
from flask import request, session, jsonify
import insta485
from insta485.api.error import InvalidUsage


def check_postid(postid):
    """Check postid."""
    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT *"
        " FROM posts"
        " WHERE postid = ?", (postid,)
    )
    if len(cur_context.fetchall()) == 0:
        raise InvalidUsage("Not Found", 404)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["GET"])
def get_comments(postid):
    """Return post on postid."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid)
    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT *"
        " FROM comments"
        " WHERE postid = ? ORDER BY commentid", (postid,)
    )
    comments = cur_context.fetchall()
    comment_list = []
    for iterator in comments:
        comment = {
            "commentid": iterator["commentid"],
            "owner": iterator["owner"],
            "owner_show_url": "/u/{}/".format(iterator["owner"]),
            "postid": postid,
            "text": iterator["text"]
        }
        comment_list.append(comment)

    context = {
        "comments": comment_list,
        "url": request.path
    }
    return jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["POST"])
def post_comments(postid):
    """Return post on postid."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid)

    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT MAX(commentid) AS commentid"
        " FROM comments"
    )
    commentid = cur_context.fetchall()[0]
    commentid = 1 if not commentid["commentid"] else commentid["commentid"] + 1

    context = {
        "commentid": commentid,
        "owner": session["username"],
        "owner_show_url": "/u/{}/".format(flask.session["username"]),
        "postid": postid,
        "text": request.json["text"]
    }

    connection.execute(
        "INSERT INTO comments (commentid, owner, postid, text) "
        "VALUES (?, ?, ?, ?)",
        (commentid, session["username"],
         postid, request.json["text"])
    )
    return flask.jsonify(**context), 201
