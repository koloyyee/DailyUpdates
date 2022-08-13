from flask import Blueprint, render_template

from ..models.portfolio import PortfolioModel

bp = Blueprint("home", __name__)


@bp.route("/")
def welcome():
    portfolioModel = PortfolioModel()
    portfolios = portfolioModel.allPortfolios()

    return render_template("home/index.html", portfolios=portfolios)
