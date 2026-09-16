from flask import Flask, send_from_directory, render_template
from flask import redirect, request, abort, url_for, session
from db import get_db, init_app
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from functools import wraps
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ['SECRET_KEY']
ADMIN_PASSWORD_HASH = os.environ['ADMIN_PASSWORD_HASH']

# закрыть соединение при ошибке
init_app(app)


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get('is_admin'):
            return redirect(url_for('login', next=request.path))
        return view(*args, **kwargs)
    return wrapped


# === Функции ===
# фильтр для изменения даты под формат
@app.template_filter('dt')
def format_dt(value, fmt='%d.%m.%Y %H:XX'):
    try:
        if isinstance(value, int):
            value = datetime.fromtimestamp(value, tz=timezone.utc)
        return value.strftime(fmt)
    except:
        return value


# === Главная ===
@app.route('/')
def index():
    return render_template('index.html')


# === Создание записки ===
@app.route('/log/create', methods = ['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        datetime = request.form['datetime']
        if title != "" and text != "":
            db = get_db()
            db.execute("INSERT INTO articles (title, text, date) VALUES (?, ?, ?)", (title, text, datetime))
            db.commit()
            return redirect(url_for('b_log'))
    
    return render_template('write.html')


# === Редактирование записки ===
@app.route('/log/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    db = get_db()
    article = db.execute(
        "SELECT * FROM articles WHERE id = ?", (article_id,)
    ).fetchone()

    if article is None:
        abort(404)

    if request.method == 'POST':
        title = request.form['title'].strip()
        text = request.form['text'].strip()
        date = request.form.get('datetime') or article['date']

        if title and text:
            db.execute(
                "UPDATE articles SET title = ?, text = ?, date = ? WHERE id = ?",
                (title, text, date, article_id)
            )
            db.commit()
            return redirect(url_for('b_log', article_id=article_id))
        
    return render_template('write.html', article=article)


# === Список записок ===
@app.route('/log')
def b_log():
    db = get_db()
    articles = db.execute(
        "SELECT * FROM articles ORDER BY id DESC"
    ).fetchall()
    return render_template('log.html', articles = articles)


# === Удаление записки ===
@app.route('/log/del/<int:article_id>', methods=['POST'])
@login_required
def del_article(article_id):
    db = get_db()
    article = db.execute(
        "SELECT id FROM articles WHERE id = ?", (article_id,)
    ).fetchone()
    if article is None:
        abort(404)

    db.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    db.commit()
    return redirect(url_for('b_log'))


# === Логин ===
@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        if check_password_hash(ADMIN_PASSWORD_HASH, password):
            session['is_admin'] = True
            session.permanent = True  # живёт дольше одной сессии        
            return redirect(url_for('index'))
        error = 'Неверный пароль'
    return render_template('login.html', error = error)


@app.route('/logout')
def logout():
    session.pop('is_admin', None)
    return redirect(url_for('index'))


# === другие страницы ===

# Статические страницы
@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory('pages', filename)


# Галерея
@app.route('/galery')
def galery():
    return abort(404)