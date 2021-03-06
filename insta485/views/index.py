"""Insta485 view."""
import os
import pathlib
import uuid
import hashlib
import arrow
import flask
from flask import request, redirect, session, url_for, send_from_directory
import insta485


# helpers


def save_file():
    """Save file."""
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)
    return uuid_basename


def delete_file(filename):
    """Delete file."""
    delete_path = os.path.join(insta485.app.config['UPLOAD_FOLDER'], filename)
    os.remove(delete_path)


def salt_password(password):
    """Generate password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return "$".join([algorithm, salt, password_hash])


def compare_password(new_password, old_password):
    """Compare password."""
    salt = old_password[7:39]
    # print(salt)
    salted_password = old_password[40:]
    hash_obj = hashlib.new('sha512')
    password_salted = salt + new_password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    # print(password_hash, salted_password)
    return password_hash == salted_password


@insta485.app.before_request
def is_login():
    """Get&before request."""
    if 'username' not in session:
        if request.endpoint in ['show_user',
                                'show_post', 'show_explore',
                                'show_edit', 'show_password', 'delete',
                                'logout_op', 'comments_op', 'like_op',
                                'posts_op', 'following_op', 'following',
                                'follower']:
            return redirect(url_for('login_page'))
    return None


@insta485.app.route('/uploads/<filename>')
def get_img(filename):
    """Get & static file permission."""
    if 'username' not in session:
        flask.abort(403)
    try:
        return send_from_directory(
            insta485.app.config['UPLOAD_FOLDER'], filename)
    except IOError:
        flask.abort(404)


@insta485.app.route('/accounts/login/')
def login_page():
    """Login page."""
    if 'username' in session:
        return redirect(url_for('index_page'))
    return flask.render_template('accounts.html')


@insta485.app.route('/')
def index_page():
    """Index page."""
    if 'username' not in session:
        return redirect(url_for('login_page'))
    config = {}
    connection = insta485.model.get_db()
    config['logname'] = session['username']
    cur_context = connection.execute(
        "SELECT *"
        " FROM posts"
        " WHERE owner = ? OR owner = (SELECT username2"
        " FROM 'following'"
        " WHERE username1 = ? )"
        " ORDER BY created, postid DESC", (str(config['logname']),
                                           str(config['logname']))
    )
    config['posts'] = cur_context.fetchall()
    for post in config['posts']:
        counter = 0
        post['islike'] = 0
        post['img_url'] = post['filename']
        post['timestamp'] = arrow.get(post['created'],
                                      'YYYY-MM-DD HH:mm:ss').humanize()
        # get owner image
        cur_tmp = connection.execute(
            "SELECT filename"
            " FROM users"
            " WHERE username = ? ", (str(post['owner']),)
        )
        post['owner_img_url'] = cur_tmp.fetchall()[0]['filename']
        # get comments
        cur_tmp = connection.execute(
            "SELECT *"
            " FROM comments"
            " WHERE postid = ? "
            " ORDER BY created, commentid DESC", (str(post['postid']),)
        )
        post['comments'] = cur_tmp.fetchall()
        # get likes
        cur_tmp = connection.execute(
            "SELECT *"
            " FROM likes"
            " WHERE postid = ? ", (str(post['postid']),)
        )
        post['likes'] = cur_tmp.fetchall()
        for like in post['likes']:
            counter = counter + 1
            if like['owner'] == config['logname']:
                post['islike'] = 1
        post['likes'] = counter
    return flask.render_template("index.html", **config)


@insta485.app.route('/u/<username>/')
def show_user(username):
    """User page."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (username,))
    user = cur.fetchall()
    if len(user) == 0:
        flask.abort(404)

    cur = connection.execute(
        "SELECT postid, filename FROM posts WHERE owner = ?",
        (username,))
    posts = cur.fetchall()

    cur = connection.execute(
        "SELECT COUNT(*) AS following FROM following WHERE username1 = ?",
        (username,))
    following_count = cur.fetchall()[0]["following"]

    cur = connection.execute(
        "SELECT count(*) AS followers FROM following WHERE username2 = ?",
        (username,))
    followers = cur.fetchall()[0]["followers"]

    cur = connection.execute(
        "SELECT count(*) AS log_follows_user FROM following WHERE "
        "username1 = ? AND username2 = ?",
        (logname, username))
    log_follows_user = cur.fetchall()[0]["log_follows_user"] == 1

    context = {"logname": logname, "username": username,
               "fullname": user[0]["fullname"], "posts": posts,
               "total_posts": len(posts), "following": following_count,
               "followers": followers, "log_follows_user": log_follows_user}

    return flask.render_template("user.html", **context)


@insta485.app.route('/p/<postid>/')
def show_post(postid):
    """Post page."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT * FROM posts WHERE postid = ?",
        (postid,))
    post = cur.fetchall()[0]

    cur = connection.execute(
        "SELECT filename FROM users WHERE username = ?",
        (post["owner"],))
    owner = cur.fetchall()[0]

    cur = connection.execute(
        "SELECT count(*) as likes FROM likes "
        "WHERE postid = ?", (postid,))
    likes = cur.fetchall()[0]["likes"]

    cur = connection.execute(
        "SELECT count(*) as log_like FROM likes WHERE postid = ? "
        "AND owner = ?", (postid, logname))
    log_like = cur.fetchall()[0]["log_like"]

    cur = connection.execute(
        "SELECT commentid, owner, created, text FROM "
        "comments WHERE postid = ?", (postid,))
    comments = cur.fetchall()

    timestamp = arrow.get(post["created"], 'YYYY-MM-DD HH:mm:ss').humanize()

    context = {"logname": logname, "postid": postid,
               "owner_filename": owner["filename"],
               "filename": post["filename"], "owner": post["owner"],
               "likes": likes, "comments": comments,
               "timestamp": timestamp, "log_like": log_like}

    return flask.render_template("post.html", **context)


@insta485.app.route('/explore/')
def show_explore():
    """Explore."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, filename FROM users WHERE username NOT IN "
        "(SELECT username2 FROM following "
        "WHERE username1 = ?) AND username != ?",
        (logname, logname))
    users = cur.fetchall()

    context = {"logname": logname, "not_following": users}

    return flask.render_template("explore.html", **context)


@insta485.app.route('/accounts/edit/')
def show_edit():
    """Accounts edit."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT filename, fullname, email FROM users WHERE username = ?",
        (logname,))
    user = cur.fetchall()[0]
    # print(user["fullname"])
    context = {"logname": logname, "filename": user["filename"],
               "fullname": user["fullname"], "email": user["email"]}

    return flask.render_template("edit.html", **context)


@insta485.app.route('/accounts/password/')
def show_password():
    """Accounts password."""
    context = {"logname": flask.session['username']}

    return flask.render_template("password.html", **context)


@insta485.app.route('/accounts/create/')
def create():
    """Create user."""
    if 'username' in session:
        return redirect(url_for('show_edit'))
    context = {}
    return flask.render_template('create.html', **context)


@insta485.app.route('/accounts/delete/')
def delete():
    """Delete user."""
    context = {"logname": flask.session['username']}
    return flask.render_template("delete.html", **context)


# Post


@insta485.app.route('/accounts/logout/', methods=['POST'])
def logout_op():
    """Logout."""
    session.clear()
    session.modified = True
    return redirect(url_for('login_page'))


@insta485.app.route('/posts/', methods=['POST'])
def posts_op():
    """Post target."""
    logname = flask.session['username']
    # print("test")
    connection = insta485.model.get_db()

    # print(request.form["operation"])
    if request.form["operation"] == "create":
        if request.files["file"].filename == "":
            flask.abort(400)

        filename = save_file()
        cur = connection.execute(
            "SELECT MAX(postid) as largest_id FROM posts")
        postid = cur.fetchall()[0]
        postid = 1 if not postid["largest_id"] else postid["largest_id"] + 1
        connection.execute(
            "INSERT INTO posts(postid, filename, owner) "
            "VALUES (?, ?, ?)", (postid, filename, logname))

    elif request.form["operation"] == "delete":
        postid = request.form["postid"]
        cur = connection.execute(
            "SELECT owner, filename FROM posts WHERE postid = ?", (postid,))
        post = cur.fetchall()
        if len(post) == 0:
            flask.abort(404)
        if post[0]["owner"] != logname:
            flask.abort(403)
        delete_file(post[0]["filename"])
        connection.execute(
            "DELETE FROM posts WHERE postid = ?", (postid,))

    url = request.args.get('target') \
        if request.args.get('target') is not None \
        else url_for("show_user", username=logname)
    return redirect(url)


@insta485.app.route('/comments/', methods=['POST'])
def comment_op():
    """Post comment."""
    connection = insta485.model.get_db()
    if request.form['operation'] == 'create':
        if request.form['text'] == "":
            flask.abort(400)
        else:
            # calculate comment_id
            cur = connection.execute(
                "SELECT *"
                " FROM comments"
                " ORDER BY commentid DESC"
            )
            com_id = cur.fetchall()[0]['commentid']
            com_id = int(com_id) + 1
            connection.execute(
                "INSERT INTO comments (commentid, owner, postid, 'text') "
                "VALUES (?, ?, ?, ?)",
                (com_id, str(session['username']),
                 str(request.form['postid']), str(request.form['text']))
            )
    else:
        cur = connection.execute(
            "SELECT *"
            " FROM comments"
            " WHERE commentid = ? AND owner = ?",
            (str(request.form['commentid']), str(session['username']))
        )
        # print(str(request.form['commentid']), str(session['username']))
        if not bool(cur.fetchall()):
            flask.abort(403)
        else:
            connection.execute(
                "DELETE"
                " FROM comments"
                " WHERE commentid = ? AND owner = ?",
                (str(request.form['commentid']), str(session['username']))
            )
    re_url = request.args.get('target') \
        if request.args.get('target') is not None \
        else url_for("index_page")
    return redirect(re_url)


@insta485.app.route('/likes/', methods=['POST'])
def like_op():
    """Post like."""
    connection = insta485.model.get_db()

    if request.form['operation'] == 'like':
        cur = connection.execute(
            "SELECT *"
            " FROM likes"
            " WHERE postid = ? AND owner = ?",
            (str(request.form['postid']), str(session['username']))
        )
        if bool(cur.fetchall()):
            flask.abort(409)
        connection.execute(
            "INSERT INTO likes (owner, postid) VALUES (?, ?)",
            (str(session['username']), str(request.form['postid']))
        )
    else:
        cur = connection.execute(
            "SELECT *"
            " FROM likes"
            " WHERE postid = ? AND owner = ?",
            (str(request.form['postid']), str(session['username']))
        )
        if not bool(cur.fetchall()):
            flask.abort(409)
        connection.execute(
            "DELETE FROM likes"
            " WHERE postid = ?"
            " AND owner = ?",
            (str(request.form['postid']), str(session['username']))
        )
    re_url = request.args.get('target') \
        if request.args.get('target') is not None \
        else url_for("index_page")
    return redirect(re_url)


@insta485.app.route('/accounts/', methods=['POST'])
def accounts_op():
    """Accounts target."""
    connection = insta485.model.get_db()
    if request.form["operation"] == "edit_account":
        edit_account()
    elif request.form["operation"] == "update_password":
        edit_password()
    elif request.form["operation"] == "login":
        login()
    elif request.form["operation"] == "delete":
        if 'username' not in session:
            flask.abort(403)
        logname = flask.session['username']
        cur = connection.execute(
            "SELECT filename FROM posts WHERE owner = ?",
            (logname,))
        files = cur.fetchall()
        for image in files:
            delete_file(image["filename"])
        cur = connection.execute(
            "SELECT filename FROM users WHERE username = ?",
            (logname,))
        filename = cur.fetchall()[0]["filename"]
        delete_file(filename)
        connection.execute(
            "DELETE FROM users WHERE username = ?",
            (str(session['username']),)
        )
        flask.session.clear()
        # return flask.redirect(flask.url_for('index_page'))
    elif request.form['operation'] == 'create':
        if 'username' in session:
            return redirect(url_for("show_edit"))
        # check if any of the provided info is empty
        if request.files["file"].filename == "" or \
                request.form["fullname"] == "" \
                or request.form["username"] == "" or \
                request.form["email"] == "" \
                or request.form["password"] == "":
            flask.abort(400)
        else:
            cur = connection.execute(
                "SELECT * FROM users WHERE username = ?",
                (str(request.form["username"]),)
            )
            if not len(cur.fetchall()) == 0:
                flask.abort(409)  # Conflict Error
            else:  # log user in and redirect to URL
                filename = save_file()
                connection.execute(
                    "INSERT INTO users (username, fullname, "
                    "email, filename, password) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (str(request.form["username"]),
                     str(request.form["fullname"]),
                     str(request.form["email"]),
                     filename,
                     salt_password(request.form["password"]))
                )
                session["username"] = request.form["username"]
    url = request.args.get('target') \
        if request.args.get('target') is not None \
        else url_for("index_page")
    return redirect(url)


def edit_account():
    """Edit account."""
    if 'username' not in session:
        flask.abort(403)
    connection = insta485.model.get_db()
    logname = flask.session['username']
    print("start")
    if request.files["file"].filename != "":
        print("nn")
        cur = connection.execute(
            "SELECT filename FROM users WHERE username = ?",
            (logname,))
        filename = cur.fetchall()[0]
        delete_file(filename["filename"])
        filename = save_file()
        connection.execute("UPDATE users SET filename = ?, "
                           "fullname = ?, email = ? "
                           "WHERE username = ?",
                           (filename, request.form["fullname"],
                            request.form["email"], logname))
    else:
        connection.execute("UPDATE users SET fullname = ?, email = ? "
                           "WHERE username = ?",
                           (request.form["fullname"],
                            request.form["email"], logname))


def edit_password():
    """Edit password."""
    if 'username' not in session:
        flask.abort(403)
    connection = insta485.model.get_db()
    logname = flask.session['username']
    if request.form["password"] == "" or \
            request.form["new_password1"] == "" \
            or request.form["new_password2"] == "":
        flask.abort(400)
    cur = connection.execute(
        "SELECT password FROM users WHERE username = ?", (logname,))
    password = cur.fetchall()[0]["password"]
    if not compare_password(request.form["password"], password):
        flask.abort(403)
    if request.form["new_password1"] != request.form["new_password2"]:
        flask.abort(401)
    connection.execute("UPDATE users SET password = ? WHERE username = ?",
                       (salt_password(request.form["new_password1"]),
                        logname))


def login():
    """Login."""
    connection = insta485.model.get_db()
    if not bool(request.form['username']) or \
            not bool(request.form['password']):
        flask.abort(400)
    cur = connection.execute(
        "SELECT *"
        " FROM users"
        " WHERE username = ?", (str(request.form['username']),))

    user = cur.fetchall()

    if len(user) == 0 or not compare_password(request.form['password'],
                                              user[0]["password"]):
        flask.abort(403)
    else:
        session['username'] = request.form['username']


@insta485.app.route('/u/<username>/followers/')
def follower(username):
    """Render follower."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (username,))
    user = cur.fetchall()
    if len(user) == 0:
        flask.abort(404)

    cur = connection.execute(
        "SELECT username, filename FROM users WHERE username in "
        "(SELECT username1 FROM following WHERE username2 = ?)", (username,))
    followers = cur.fetchall()

    cur = connection.execute(
        "SELECT username2 FROM following "
        "WHERE username1 = ? AND username2 in "
        "(SELECT username1 FROM following "
        "WHERE username2 = ?)", (logname, username))
    logname_following = cur.fetchall()
    tmp = []
    for log_follow in logname_following:
        tmp.append(log_follow["username2"])

    context = {"logname": logname, "username": user[0]["username"],
               "followers": followers, "logname_following": tmp}

    return flask.render_template("followers.html", **context)


@insta485.app.route('/u/<username>/following/')
def following(username):
    """Render follower."""
    logname = flask.session['username']
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT username, fullname FROM users WHERE username = ?",
        (username,))
    user = cur.fetchall()
    if len(user) == 0:
        flask.abort(404)
    cur = connection.execute(
        "SELECT username, filename FROM users WHERE username in "
        "(SELECT username2 FROM following WHERE username1 = ?)", (username,))
    followings = cur.fetchall()

    cur = connection.execute(
        "SELECT username2 FROM following "
        "WHERE username1 = ? AND username2 in "
        "(SELECT username2 FROM following "
        "WHERE username1 = ?)", (logname, username))
    logname_following = cur.fetchall()
    tmp = []
    for log_follow in logname_following:
        tmp.append(log_follow["username2"])

    context = {"logname": logname, "username": user[0]["username"],
               "following": followings, "logname_following": tmp}

    return flask.render_template("following.html", **context)


@insta485.app.route('/following/', methods=['POST'])
def following_op():
    """Handle following."""
    connection = insta485.model.get_db()
    if request.form['operation'] == 'follow':
        cur = connection.execute(
            " SELECT *"
            " FROM following"
            " WHERE username2 = ? AND username1 = ?",
            (str(request.form['username']), (str(session['username']))))
        if len(cur.fetchall()) != 0:
            flask.abort(409)
        connection.execute(
            "INSERT INTO following (username1, username2) VALUES (?, ?)",
            (str(session['username']), str(request.form['username']))
        )
    else:
        cur = connection.execute(
            " SELECT *"
            " FROM following"
            " WHERE username2 = ? AND username1 = ?",
            (str(request.form['username']), (str(session['username']))))
        if len(cur.fetchall()) == 0:
            flask.abort(409)
        connection.execute(
            "DELETE FROM following WHERE username1 = ? AND username2 = ?",
            (str(session['username']), str(request.form['username']))
        )
    re_url = request.args.get('target') \
        if request.args.get('target') is not None \
        else url_for("index_page")
    return redirect(re_url)
