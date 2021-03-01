PRAGMA foreign_keys = ON;

CREATE TABLE users
(
    username VARCHAR(20),
    fullname VARCHAR(40)  NOT NULL,
    email    VARCHAR(40)  NOT NULL,
    filename VARCHAR(64)  NOT NULL,
    password VARCHAR(256) NOT NULL,
    created  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username)
);

CREATE TABLE posts
(
    postid   INTEGER,
    filename VARCHAR(64) NOT NULL,
    owner    VARCHAR(20) NOT NULL,
    created  DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (postid),
    FOREIGN KEY (owner) REFERENCES users (username)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE following
(
    username1 VARCHAR(20) NOT NULL,
    username2 VARCHAR(20) NOT NULL,
    created   DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (username1, username2),
    FOREIGN KEY (username1) REFERENCES users (username)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (username2) REFERENCES users (username)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE comments
(
    commentid INTEGER,
    owner     VARCHAR(20)   NOT NULL,
    postid    INTEGER       NOT NULL,
    created   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    text      VARCHAR(1024) NOT NULL,
    PRIMARY KEY (commentid),
    FOREIGN KEY (owner) REFERENCES users (username)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (postid) REFERENCES posts (postid)
        ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE likes
(
    owner   VARCHAR(20) NOT NULL,
    postid  INTEGER     NOT NULL,
    created DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (owner, postid),
    FOREIGN KEY (owner) REFERENCES users (username)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (postid) REFERENCES posts (postid)
        ON UPDATE CASCADE ON DELETE CASCADE
);
