"""Insta485 REST API."""

from insta485.api.likes import get_likes, post_likes, delete_likes
from insta485.api.posts import get_post
from insta485.api.comments import get_comments, post_comments
from insta485.api.error import handle_invalid_usage, is_login



