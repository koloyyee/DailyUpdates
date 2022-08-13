"""
Query for portfolio.json.
"""
import json

from flask import flash

with open('dailyUpdates/schema/portfolio.json', "rb") as f:
    portfolios = json.load(f)


class PortfolioModel():
    def allPortfolios(self):
        try:
            if portfolios:
                return portfolios
        except:
            return flash("no data", "message")
