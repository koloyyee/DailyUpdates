from flask import Blueprint, render_template

bp = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@bp.route("/")
def portfolios():
    return render_template("portfolio/index.html")
