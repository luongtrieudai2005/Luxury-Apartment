import sqlite3
from flask import g, current_app

def get_db():
    """Get a SQLite connection stored in flask.g (one per request)."""
    if "db" not in g:
        db_path = current_app.config["DB_PATH"]
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        g.db = conn
    return g.db

def close_db(e=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()

def init_app(app):
    app.teardown_appcontext(close_db)
