import sqlite3
from flask import g

DATABASE = 'base.db'

def get_db():
    """Возвращает соединение с БД, создавая его при необходимости."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # доступ к колонкам по имени
    return g.db

def close_db(e=None):
    """Закрывает соединение в конце запроса."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Регистрирует закрытие БД в приложении."""
    app.teardown_appcontext(close_db)