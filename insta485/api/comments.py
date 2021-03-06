"""REST API for comments."""
import flask
import insta485
from flask import request, session, jsonify
from insta485.api.error import InvalidUsage


def check_postid(postid):
    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT *"
        " FROM posts"
        " WHERE postid = ?", (postid,)
    )
    if not len(cur_context.fetchall()):
        raise InvalidUsage("Not Found", 404)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["GET"])
def get_comments(postid):
    """Return post on postid.

    Example:
    {
  "comments": [
    {
      "commentid": 1,
      "owner": "awdeorio",
      "owner_show_url": "/u/awdeorio/",
      "postid": 3,
      "text": "#chickensofinstagram"
    },
    {
      "commentid": 2,
      "owner": "jflinn",
      "owner_show_url": "/u/jflinn/",
      "postid": 3,
      "text": "I <3 chickens"
    },
    {
      "commentid": 3,
      "owner": "michjc",
      "owner_show_url": "/u/michjc/",
      "postid": 3,
      "text": "Cute overload!"
    }
  ],
  "url": "/api/v1/p/3/comments/"
}
    """
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
    for i in range(len(comments)):
        comment = {
            "commentid": comments[i]["commentid"],
            "owner": comments[i]["owner"],
            "owner_show_url": "/u/{}/".format(comments[i]["owner"]),
            "postid": postid,
            "text": comments[i]["text"]
        }
        comment_list.append(comment)

    context = {
        "comments": comment_list,
        "url": request.path
    }
    return jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["POST"])
def post_comments(postid):
    """Return post on postid.

    Example:
    {
  "comments": [
    {
      "commentid": 1,
      "owner": "awdeorio",
      "owner_show_url": "/u/awdeorio/",
      "postid": 3,
      "text": "#chickensofinstagram"
    },
    {
      "commentid": 2,
      "owner": "jflinn",
      "owner_show_url": "/u/jflinn/",
      "postid": 3,
      "text": "I <3 chickens"
    }
  ],
  "url": "/api/v1/p/3/comments/"
}
    """
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    check_postid(postid)

    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT MAX(commentid) AS commentid"
        " FROM comments"
    )
    commentid = cur_context.fetchall()
    commentid = 1 if not commentid else commentid[0]["commentid"] + 1

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
