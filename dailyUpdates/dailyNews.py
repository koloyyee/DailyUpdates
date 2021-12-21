import json
import os

from flask import Blueprint, Flask, flash, g, render_template

from dailyUpdates.Models.news import NewsModel

# from scrapeNews import BBCnews, CNNnews, FinvizNews

bp = Blueprint("dailyNews", __name__)

# retrieve all


@bp.route("/")
def allNews():
    newsModel = NewsModel()
    news = newsModel.allNews()
    allNewsKey = ["headline", "url", "agency"]
    data = []
    for n in news:
        data.append(dict(zip(allNewsKey, n)))

    return render_template("news/index.html", allNews=data)


@bp.route("/<agency>")
def agencyNews(agency: str):
    newsModel = NewsModel()
    news = newsModel.allNewsByAgency(agency.strip().lower())
    allNewsKey = ["headline", "url", "agency"]
    data = []
    for n in news:
        data.append(dict(zip(allNewsKey, n)))
    return render_template("news/agency.html", allNews=data)
