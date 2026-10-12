import sqlite3

DATABASE = 'base.db'

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT NOT NULL,
    text     TEXT NOT NULL,
    imgpath  TEXT,
    date     INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE TABLE IF NOT EXISTS links (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    description TEXT,
    url         TEXT NOT NULL,
    title      TEXT NOT NULL
);
"""

def init():
    conn = sqlite3.connect(DATABASE)
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"БД {DATABASE} инициализирована.")

if __name__ == '__main__':
    init()