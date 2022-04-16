
import pathlib

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from markdown2 import Markdown, markdown, markdown_path
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from dailyUpdates.auth import loginRequired
from dailyUpdates.Models.blog import BlogModel

md = Markdown(extras={"fenced-code-blocks": None})

base_dir = pathlib.Path(__file__).absolute().parent
postsDir = base_dir/"posts"

bp = Blueprint("blog", __name__)
# bp = Blueprint("blog", __name__, url_prefix="/blog")


# @bp.route("/", methods=["GET"])
# def allPostsTitle():
#     """
#     return all posts titles from markdown files.
#     """
#     posts = []
#     dates = sorted(
#         [p for p in postsDir.iterdir() if p.name != "draft"],
#         key=lambda p: [int(y.lstrip("0")) for y in p.name.split("-")],
#         reverse=True
#     )
#     for date in dates:
#         postPath = list(date.iterdir())[0]

#         with postPath.open("r") as f:
#             post = {}
#             t = f.readline().strip('\n# ')
#             post["title"] = t
#             post["date"] = date.name
#             post["postPath"] = postPath
#         posts.append(post)
#     if posts:
#         return render_template("blog/index.html", posts=posts)


@bp.route("/", methods=["GET"])
def BlogPostsTitle():
    blog = BlogModel()
    posts = blog.retrievePosts()
    return render_template("blog/index.html", posts=posts)


@bp.route("/<string:title>", methods=["GET"])
def blogPost(title: str):
    blog = BlogModel()
    print(title)
    post = blog.retrievePosts(title)
    return render_template("blog/post.html", post=post)

# @bp.route("/<string:date>/<string:post>", methods=["GET"])
# def blogPost(date: str, post: str):
#     markdownFile = postsDir / date / f"{post}.md"
#     with markdownFile.open("r") as f:
#         text = f.read()
#         _, text = text.split("\n", 1)
#     html = md.convert(text)
#     return render_template(
#         "blog/post.html",
#         blogTitle=post,
#         blogDate=date,
#         blogContent=html

#     )


class ContentForm(FlaskForm):
    title = StringField("title", name="title", validators=[DataRequired()])
    content = CKEditorField("content", name="content",
                            validators=[DataRequired()])
    submit = SubmitField("submit")


@bp.route("/create", methods=["POST", "GET"])
@loginRequired
def create():
    form = ContentForm()
    blog = BlogModel()

    if request.method == "POST":
        # request.form[] <-- originally by flask
        # form. <-- flask-wtf

        title = form.title.data
        content = form.content.data
        id = session["user_id"]
        # if title and content:
        blog.createPost(id, title, content)
    # if form.validate_on_submit():
        return redirect("/")
    return render_template("blog/create.html", form=form)
