"""
Query for agencies table.
"""
from typing import List

from dailyUpdates.db import getDB
from flask import abort


class AgencyModel():
    # Create
    def registerAgency(self, agency: str, url: str) -> None:
        """
        :param - agency :str, name of the news agency
        :param - url: str, link to the news page, not including which category.
        """
        db = getDB()
        db.execute(
            "INSERT INTO agency (agency, url) VALUES (?, ?)", (agency, url)
        )
        db.commit()

    # Retrieve All

    def getAllAgencies(self) -> List[str]:
        db = getDB()
        agencies = db.execute(
            "SELECT * from agency"
        ).fetchall()
        db.commit
        return agencies

    # Retrieve by id

    def getAgency(self, id: int) -> str:
        db = getDB()
        agency = db.execute(
            "SELECT * from agency WHERE id = ?", (id,)
        ).fetchone()
        if agency is None:
            abort(404, f"Agency doesn't exist")
        return agency

    # Update

    def updateAgency(self, agency: str, url: str, id: int) -> str:
        newAgency = self.getAgency(id)
        db = getDB()
        db.execute(
            "UPDATE agency SET agency = ?, url = ? WHERE id = ?", (
                agency, url, id)
        )
        db.commit()
        return newAgency
