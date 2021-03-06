"""REST API for posts."""
import flask
from flask import request, jsonify, session
import insta485
from insta485.api.error import InvalidUsage
from insta485.api.comments import check_postid


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
def get_post(postid):
    """Return post on postid."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    connection = insta485.model.get_db()
    check_postid(postid)
    cur_context = connection.execute(
        "SELECT postid, filename, owner, created"
        " FROM posts"
        " WHERE postid = ?", (postid,)
    )

    post = cur_context.fetchall()
    if len(post) == 0:
        raise InvalidUsage("Not Found", 404)
    post = post[0]

    cur_context = connection.execute(
        "SELECT *"
        " FROM users"
        " WHERE username = ?", (post["owner"],)
    )

    owner = cur_context.fetchall()[0]

    context = {
        "age": post["created"],
        "img_url": "/uploads/{}".format(post["filename"]),
        "owner": post["owner"],
        "owner_img_url": "/uploads/{}".format(owner["filename"]),
        "owner_show_url": "/u/{}/".format(post["owner"]),
        "post_show_url": "/p/{}/".format(postid),
        "url": request.path
    }
    return jsonify(**context)


@insta485.app.route('/api/v1/', methods=["GET"])
def get_service():
    """Return a list of services available."""
    context = {
        "posts": "/api/v1/p/",
        "url": "/api/v1/"
    }
    return jsonify(**context)


@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_ten_posts():
    """Return the 10 newest posts."""
    if 'username' not in session:
        raise InvalidUsage('Forbidden', status_code=403)
    connection = insta485.model.get_db()
    users = flask.session["username"]
    post_size = flask.request.args.get("size", default=10, type=int)
    page_size = flask.request.args.get("page", default=0, type=int)
    if page_size < 0 or post_size < 0:
        raise InvalidUsage("Bad Request", 400)

    offset = page_size * post_size

    cur_context = connection.execute(
        "SELECT DISTINCT p.postid"
        " FROM posts p, users u"
        " WHERE ("
        " p.owner = ?"
        " OR p.owner IN"
        " (SELECT username2 FROM following"
        " WHERE username1 = ?)"
        " AND p.owner = u.username)"
        " ORDER BY p.postid DESC"
        " LIMIT ? OFFSET ?", (str(users), str(users), post_size + 1, offset)
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
