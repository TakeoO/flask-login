import json

from flask import render_template, request, Blueprint, url_for

from models.user import User
from utils.user_helper import redirectToRoute, redirectToLogin, getCurrentUser, redirect, make_response, isLoggedIn
from models.settings import db
from models.post import Post
from models.comment import Comment

post_handlers = Blueprint("post", __name__)


@post_handlers.route('/post-add-form', methods=["GET"])
def post_form():
    return render_template("post_add_form.html") if isLoggedIn() else redirectToLogin()


@post_handlers.route('/post/<id>', methods=["GET", "DELETE", "POST"])
def handle_post(id):
    post = db.query(Post).filter_by(id=id).first()
    return render_template("post.html", post=post, comments=db.query(Comment).filter_by(post=post).all())
    # redirect to 404


@post_handlers.route('/post', methods=["POST"])
def createPost():
    title = request.form.get('title')
    description = request.form.get('description')
    author = getCurrentUser()

    Post.create(title=title, description=description, author=author)

    return redirectToRoute("dashboard.dashboard")


@post_handlers.route("/add-comment/<post_id>", methods=["POST"])
def addComment(post_id):
    if isLoggedIn():
        comment = request.form.get("comment")
        redisObjectUser = json.loads(getCurrentUser())
        post = db.query(Post).filter_by(id=post_id).first()
        author = db.query(User).filter_by(email=redisObjectUser["email"]).first()

        if not post:
            return make_response(redirect(url_for("dashboard.dashboard"), code=404))

        Comment.create(comment, post, author)
        return make_response(redirect(url_for("post.handle_post", id=post_id)))
    else:
        return redirectToLogin()
