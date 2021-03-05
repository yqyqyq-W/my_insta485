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


@insta485.app.route('/api/v1/', methods=["GET"])
def get_service():
    """Return a list of services available.
    The output should look exactly like this example.
    {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }"""
    context = {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    return jsonify(**context)

@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_ten_posts():
    """Return the 10 newest posts.
     The posts should meet the following criteria:
     each post is made by a user which the logged in user
     follows or the post is made by the logged in user.
     The URL of the next page of posts is returned in next.
     Note that postid is an int, not a string.

     {
        "next": "",
        "results": [
        {
            "postid": 3,
            "url": "/api/v1/p/3/"
        },
        {
            "postid": 2,
            "url": "/api/v1/p/2/"
        },
        {
            "postid": 1,
            "url": "/api/v1/p/1/"
        }
        ],
        "url": "/api/v1/p/"
    }"""

    connection = insta485.model.get_db()
    users = session["user"]
    post_size = flask.request.args.get("size", default=10, type=int)
    page_size = flask.request.args.get("page", default=10, type=int)
    if page_size < 0 or post_size < 0:
        raise handle_invalid_usage("Bad Request", 400)

    offset = page_size * post_size

    cur_context = connection.execute(
        "SELECT DISTINCT p.postid"
        " FROM posts p, users u"
        " WHERE ("
        "p.owner = '{}'"
        "OR p.owner IN "
        "(SELECT username2 FROM following"
        "WHERE username1 = '{}')"
        "AND p.owner = u.username)"
        "ORDER BY p.postid DESC"
        "LIMIT {} OFFSET {}".format(str(users), str(users), post_size + 1, offset)
    )
    
    posts = cur_context.fetchall()
    url_next = ""

    if len(posts) == post_size + 1:
        url_next = "/api/v1/p/?size={}&page={}".format(post_size, page_size+1)
        posts.pop()

    result_list = []
    for post in posts:
        result = {
            "postid": post["postid"],
            "url": "/api/v1/p/{}/".format(post["postid"])
        }
        result_list.append(result)

    context = {
        "next": url_next,
        "results": result_list,
        "url": flask.request.path
    }
    return jsonify(**context)