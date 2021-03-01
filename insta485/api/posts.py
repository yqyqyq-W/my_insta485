"""REST API for posts."""
import flask
import insta485
from flask import request, jsonify


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
def get_post(postid):
    """Return post on postid.

    Example:
    {
      "age": "2017-09-28 04:33:28",
      "img_url": "/uploads/122a7d27ca1d7420a1072f695d9290fad4501a41.jpg",
      "owner": "awdeorio",
      "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "owner_show_url": "/u/awdeorio/",
      "post_show_url": "/p/1/",
      "url": "/api/v1/p/1/"
    }
    """
    connection = insta485.model.get_db()
    cur_context = connection.execute(
        "SELECT *"
        " FROM posts"
        " WHERE postid = ?", (postid,)
    )

    post = cur_context.fetchall()
    if not len(post):
        raise Exception("Not Found", 404)

    context = {
        "age": post["created"],
        "img_url": post["filename"],
        "owner": post["owner"],
        "owner_img_url": "/uploads/" + post["filename"],
        "owner_show_url": "/u/{}/".format(post["owner"]),
        "postid": "/p/{}/".format(postid),
        "url": request.path
    }
    return jsonify(**context)
