"""
Query for register or login

"""


from webbrowser import get

import dailyUpdates
from flask import abort, redirect, session, url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import getDB


class User():

    def register(self, username: str, password: str) -> None:
        db = getDB()
        db.execute(
            "INSERT INTO users ( username, password) VALUES (?, ?)", (
                username, generate_password_hash(password))
        )
        db.commit()

    def login(self, username: str, password: str):
        db = getDB()
        error = None
        user = db.execute(
            "SELECT * FROM users WHERE username = ? ", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user['id']
            return True
        else:
            return error

    def user(self, username: str):
        """
        :param - input username
        :return - user id
        """
        db = getDB()
        user = db.execute(
            "SELECT id FROM users WHERE username = ?", (username,)
        ).fetchone()

        if user:
            return user

    def gUser(self, id):
        db = getDB()
        return db.execute(
            "SELECT * FROM users WHERE id = ?", (id)
        ).fetchone()
