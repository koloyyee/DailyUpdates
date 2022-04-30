
from celery.schedules import crontab

from . import scrape
from .celery import app

# how to schedule tasks with celery beat_schedule
# next we will set up schedule to fetch or scrape news from CNN, BBC, and Finviz.


@app.task
def allNews(agencyUrl: list[str], category: list[str] = None) -> None:
    """
    :params: agencyUrl - list of url of the new agency to be scraped.
    :params: category - category of news to be scrape, default = None.
    :return: None, values will be inserted into the db directly.
    """
    for agency in agencyUrl:
        print(f"fetching news from {agency}")
        news = scrape.AgencyNews(agency)

        if agency == "https://finviz.com" or agency == "https://www.reuters.com":
            news.fetchNews()
        else:
            for c in category:
                print(f"fetching {agency} - {c}")
                news.fetchNews(c)
        # news.fetchNews()
