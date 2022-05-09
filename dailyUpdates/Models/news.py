"""
Query for news table.
"""
from dailyUpdates.db import getDB
from flask import abort


class NewsModel():

    # Retrieve latest 20
    def allNews(self):
        db = getDB()
        news = db.execute(
            "SELECT headline, n.url, a.agency from news n JOIN agency a ON n.agency_id = a.id ORDER BY n.id DESC"
        ).fetchall()
        db.commit()
        return news

    def allNewsByAgencyID(self, id):
        db = getDB()
        news = db.execute(
            " SELECT * from news WHERE agency_id = ? ", (id,)
        ).fetchone()
        if news is None:
            abort(404)
        return news

    def allNewsByAgency(self, agency):
        db = getDB()
        news = db.execute(
            " SELECT headline, n.url, a.agency from news n JOIN agency a WHERE a.agency = ? and n.agency_id = a.id order by created desc limit 100", (
                agency,)
        ).fetchall()
        if news is None:
            abort(404)
        return news
