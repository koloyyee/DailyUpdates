import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def getDB():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def closeDB(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# Run the db
def initDB():
    db = getDB()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command("initDB")
@with_appcontext
def initDBCommand():
    """ Clear the existing data and create a database."""
    initDB()
    click.echo("Initialized the database.")


def initApp(app):
    app.teardown_appcontext(closeDB)
    app.cli.add_command(initDBCommand)
