import json
import os

from flask import (Blueprint, Flask, flash, g, jsonify, redirect,
                   render_template)
from flask.helpers import url_for

from dailyUpdates.Models.agencies import AgencyModel
from dailyUpdates.Models.news import NewsModel

# from scrapeNews import BBCnews, CNNnews, FinvizNews

# bp = Blueprint("dailyNews", __name__)
bp = Blueprint("dailyNews",  __name__, url_prefix="/news")
# retrieve all


@bp.route("/")
def mySubscriptions():
    agencyModel = AgencyModel()
    agencies = agencyModel.getAllAgencies()

    return render_template("news/index.html", agencies=agencies)


@bp.route("/json")
def jsonTest():
    newsModel = NewsModel()
    news = newsModel.allNews()
    allNewsKey = ["headline", "url", "agency"]
    data = []
    for n in news:
        data.append(dict(zip(allNewsKey, n)))
    return jsonify(data)


@bp.route("/<string:agency>")
def agencyNews(agency: str):
    newsModel = NewsModel()
    news = newsModel.allNewsByAgency(agency.strip().lower())
    allNewsKey = ["headline", "url", "agency"]
    data = []
    for n in news:
        data.append(dict(zip(allNewsKey, n)))
    if len(data) == 0:
        return redirect(url_for("agency.register"))
    return render_template("news/agency.html", allNews=data)
