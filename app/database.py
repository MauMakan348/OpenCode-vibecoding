import sqlite3

import click
from flask import current_app, g


def get_db():
    """Return a SQLite connection for the current request/app context."""
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(exception=None):
    """Close the SQLite connection at the end of the app context."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Create all tables from the schema file."""
    db = get_db()
    with current_app.open_resource("schema.sql") as schema_file:
        db.executescript(schema_file.read().decode("utf-8"))
    db.commit()


@click.command("init-db")
def init_db_command():
    """Create the SQLite tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
