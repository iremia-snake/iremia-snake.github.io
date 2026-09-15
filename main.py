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



# фильтр для изменения даты под формат
@app.template_filter('dt')
def format_dt(value, fmt='%d.%m.%Y %H:XX'):
    try:
        if isinstance(value, int):
            value = datetime.fromtimestamp(value, tz=timezone.utc)
        return value.strftime(fmt)
    except:
        return value


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/write', methods = ['GET', 'POST'])
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


@app.route('/log')
def b_log():
    db = get_db()
    articles = db.execute(
        "SELECT * FROM articles ORDER BY date DESC"
    ).fetchall()
    # articles = [
    #     {**dict(row), 'date': datetime.strftime(row['date'], '%d.%m.%Y %H:XX')}
    #     for row in rows
    # ]
    return render_template('log.html', articles = articles)

@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory('pages', filename)

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