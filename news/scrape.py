"""
Scraping BBC, CNN, and Finviz business news

"""
import os
from datetime import date
from typing import List, Tuple

import urllib3
from bs4 import BeautifulSoup
from dailyUpdates import create_app
from dailyUpdates.db import getDB, initDB
from flask import abort
from pydantic import UrlUserInfoError


class AgencyNews():
    def __init__(self, url: str) -> None:
        self.url = url

    def fetchNews(self, category: str = None):
        http = urllib3.PoolManager()
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (HTML, like Gecko) Version/13.1.1 Safari/604.1'}

        if category:
            r = http.request("GET", f"{self.url}/{category}", headers=headers)
            print(f"{self.url}/{category}")
        elif category == None and self.url in "http://www.finviz.com":
            r = http.request("GET", f"{self.url}/news.ashx", headers=headers)
        else:
            r = http.request("GET", f"{self.url}", headers=headers)
        feature = "lxml"

        # feature = "html.parser"

        parsed = BeautifulSoup(r.data, feature)

        if self.url == "https://www.bbc.com/news":  # BBC
            headlines = parsed.find_all(class_="gs-c-promo-heading")[1:-12]
        elif self.url in "https://edition.cnn.com":  # CNN
            headlines = parsed.find_all("h3", class_="cd__headline")
        elif self.url in "https://finviz.com":  # finviz
            headlines = parsed.find_all(class_="nn-tab-link")
        else:  # Reuters
            headlines = parsed.find_all(class_="heading__base__2T28j")
        print(len(headlines))

        titles, urls = self.getHeadlines(headlines)

        app = create_app()

        with app.app_context():
            populateDB(titles, urls, self.url)

    def getHeadlines(self, headlines: list[str]):
        titles = []
        urls = []

        for h in headlines:
            if h.get("href") is not None:
                titles.append(h.get_text())
                if self.url == "https://edition.cnn.com":
                    urls.append(h.a.get("href"))
                urls.append(h.get("href"))
        print(headlines)
        return titles, urls


class BBCnews():
    BBC_URL = "https://www.bbc.com/news"

    def getNews(self, category: str):
        """
        :params - takes news category as an argument, do not have "/".
        :return - a json file with [{"title": title, "url": url}]
        """
        app = create_app()

        http = urllib3.PoolManager()
        r = http.request("GET", f"{self.BBC_URL}/{category}")
        rd = r.data
        parsed = BeautifulSoup(rd, "html.parser")

        # excluded the last 7 because of the url, and those are permanent articles.
        headlines = parsed.find_all(class_="gs-c-promo-heading")[1:-12]

        titles, urls = self.BBCheadlines(headlines)

        # self.newsToJSON(titles, urls, category)
        with app.app_context():

            populateDB(titles, urls, self.BBC_URL)

    def BBCheadlines(self, headlines: List[str]) -> Tuple[List[str], List[str]]:
        titles = []
        urls = []
        for h in headlines:
            titles.append(h.get_text())
            urls.append(h.get("href"))
        return titles, urls


class CNNnews():
    CNN_URL = "https://edition.cnn.com"
    """
    :params - takes news category as an argument, do not have "/".
    :return - a json file with [{"title": title, "url": url}]
    """

    def getNews(self, category: str):
        app = create_app()
        http = urllib3.PoolManager()

        r = http.request("GET", f"{self.CNN_URL}/{category}")
        parsed = BeautifulSoup(r.data, "html.parser")
        headlines = parsed.find_all(class_="cd__headline")

        titles, urls = self.CNNheadlines(headlines)
        # self.newsToJSON(titles, urls, category)
        with app.app_context():
            populateDB(titles, urls, self.CNN_URL)

    def CNNheadlines(self, headlines: List[str]) -> Tuple[List[str], List[str]]:

        titles = []
        urls = []

        for h in headlines:
            titles.append(h.get_text())
            urls.append(h.a.get("href"))

        return titles, urls


class FinvizNews():

    FINVIZ_URL = "https://finviz.com"

    def finvizTickerNews(self, ticker: str):
        http = urllib3.PoolManager()

        # adding headers to pass the cloudflare bot blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/604.1'}
        # must have headers = headers because the request 3rd argument is field
        tickerLink = f"{self.FINVIZ_URL}quote.ashx?t={ticker}"
        r = http.request(
            "GET", tickerLink, headers=headers)
        parsed = BeautifulSoup(r.data, "lxml")

        # finviz news agency headlines.
        headlines = parsed.find_all(class_="news-link-container")

        titles, urls = self.headlines(headlines)
        self.newsToJSON(titles, urls, ticker)

    def finvizDaily(self):
        # https://finviz.com/news.ashx
        http = urllib3.PoolManager()
        # create_app helps to connect with the sqlite3 db
        app = create_app()

        # adding headers to pass the cloudflare bot blocking
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/604.1'}
        # must have headers = headers because the request 3rd argument is field

        generalLink = f"{self.FINVIZ_URL}/news.ashx"
        r = http.request(
            "GET", generalLink, headers=headers)
        parsed = BeautifulSoup(r.data, "lxml")

        # finviz news agency headlines.
        headlines = parsed.find_all(class_="nn-tab-link")

        titles, urls = self.headlines(headlines)
        # self.newsToJSON(titles, urls)

        with app.app_context():
            populateDB(titles, urls, self.FINVIZ_URL)

    def headlines(self, headlines: List[str]) -> Tuple[List[str], List[str]]:
        titles = []
        urls = []
        for h in headlines[1:]:
            titles.append(h.get_text())
            urls.append(h.get("href"))
        return (titles, urls)


class Reuters():
    REUTERS = "https://www.reuters.com"

    def reutersNews(self):
        http = urllib3.PoolManager()

        app = create_app()
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/604.1'}

        r = http.request("GET", self.REUTERS, headers=headers)
        parsed = BeautifulSoup(r.data, "lxml")

        headlines = parsed.find_all(class_="heading__base__2T28j")
        titles, urls = self.reutersHeadlines(headlines=headlines)

        with app.app_context():
            populateDB(titles, urls, self.REUTERS)

    def reutersHeadlines(self, headlines: list[str]) -> Tuple[List[str], List[str]]:
        titles = []
        urls = []
        for h in headlines[1:-9]:
            titles.append(h.get_text())
            urls.append(h.get("href"))

        print(f"Reuters: {titles}, {urls}")
        return (titles, urls)


def getAgency(url: str) -> int:
    """
    Query the agency id according to the new agency url.
    This is used by different news agency class.
    :param - url is the agency url which was register in the agency/register.html
    return int

    """
    db = getDB()
    print(os.path.dirname(os.path.abspath(__file__)))
    id = db.execute(
        "SELECT id, agency, url FROM agency WHERE url = ? ", (url,)
    ).fetchone()
    if id is None:
        abort(404, f"Agency doesn't exist.")

    # id was sqlite3.Row object, [0] will return an int value.
    return id[0]


def populateDB(titles: List[str], urls: List[str], agencyURL: str) -> None:
    """
    This insert into the sqlite3 db.
    """
    id = getAgency(agencyURL)
    db = getDB()
    # finviz == 3
    if "finviz" in agencyURL:
        for link in zip(titles, urls):
            db.execute(
                "INSERT INTO news (headline, url, agency_id) VALUES (?, ?, ?) ", (
                    link[0], link[1], id,)
            )
            db.commit()
    elif "cnn" in agencyURL or "reuters" in agencyURL:
        for link in zip(titles, urls):
            # fullLink is the combining the new agency url with the url scrape from the site.
            fullLink = f"{agencyURL}{link[1]}"
            db.execute(
                "INSERT INTO news (headline, url, agency_id) VALUES (?, ?, ?) ", (
                    link[0], fullLink, id,)
            )
            db.commit()
    elif "bbc" in agencyURL:
        for link in zip(titles, urls):
            if link[1] is not None:
                cleaned = link[1].replace("/news", "")
                fullLink = f"{agencyURL}{cleaned}"
                db.execute(
                    "INSERT INTO news (headline, url, agency_id) VALUES (?, ?, ?) ", (
                        link[0], fullLink, id,)
                )
                db.commit()
