
from celery.schedules import crontab

from . import scrape
from .celery import app


# how to schedule tasks with celery beat_schedule
# next we will set up schedule to fetch or scrape news from CNN, BBC, and Finviz.
@app.task
def cnn(categories: list[str]) -> None:
    print(f"fetching CNN {categories}.")
    cnn = scrape.CNNnews()
    for c in categories:
        cnn.getNews(c)


@app.task
def bbc(categories: list[str]) -> None:
    print(f"fetching BBC {categories}")
    bbc = scrape.BBCnews()
    for c in categories:
        bbc.getNews(c)


@app.task
def finviz(ticker: str = None) -> None:
    print(f"fetching finviz news")
    finviz = scrape.FinvizNews()
    if ticker is True:
        finviz.finvizTickerNews(ticker)
    finviz.finvizDaily()
