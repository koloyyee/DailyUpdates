"""
Query for blog table

"""

from typing import List

from dailyUpdates.auth import login_user
from dailyUpdates.db import getDB
from flask import flash


class BlogModel():
    # Create
    # Retrieve
    # Update
    # Delete

    def createPost(self, id: int, title: str, content: str) -> None:

        db = getDB()
        try:

            db.execute(
                "INSERT INTO post (author_id, title, body) VALUES(?,?,?)", (id,
                                                                            title, content)
            )
            db.commit()
        except ValueError:
            db.rollback()
            flash(message="insert error.")

    def retrievePosts(self, title: str = None) -> list or str:
        db = getDB()
        if title is None:
            return db.execute("SELECT * FROM post").fetchall()

        else:
            return db.execute(
                "SELECT * FROM post where title = ?", (title,)).fetchone()
