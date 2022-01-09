import os
import pathlib
import re
from datetime import datetime

from flask import Blueprint, render_template
from markdown2 import Markdown, markdown, markdown_path

md = Markdown(extras={"fenced-code-blocks": None})

base_dir = pathlib.Path(__file__).absolute().parent
postsDir = base_dir/"posts"


bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/", methods=["GET"])
def allPostsTitle():
    """
    return all posts titles from markdown files.
    """
    posts = []
    dates = sorted(
        [p for p in postsDir.iterdir() if p.name != "draft"],
        key=lambda p: [int(y.lstrip("0")) for y in p.name.split("-")],
        reverse=True
    )
    for date in dates:
        postPath = list(date.iterdir())[0]

        with postPath.open("r") as f:
            post = {}
            t = f.readline().strip('\n# ')
            post["title"] = t
            post["date"] = date.name
            post["postPath"] = postPath
        posts.append(post)
    if posts:
        return render_template("blog/index.html", posts=posts)


@bp.route("/<string:date>/<string:post>", methods=["GET"])
def blogPost(date: str, post: str):
    markdownFile = postsDir / date / f"{post}.md"
    with markdownFile.open("r") as f:
        text = f.read()
        _, text = text.split("\n", 1)
    html = md.convert(text)
    return render_template(
        "blog/post.html",
        blogTitle=post,
        blogDate=date,
        blogContent=html

    )
