from flask import Flask, send_from_directory, render_template
from flask import redirect, request, abort, url_for, session
from db import get_db, init_app
from datetime import datetime, timezone
import os
from os import path
import uuid
from dotenv import load_dotenv
from functools import wraps
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ['SECRET_KEY']
ADMIN_PASSWORD_HASH = os.environ['ADMIN_PASSWORD_HASH']

# параметры загружаемых изображений
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = ('png', 'jpg', 'jpeg', 'gif', 'webp')

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


# получение ссылки через контект-процессор
@app.context_processor
def inject_links():
    db = get_db()
    outer_links = db.execute(
        "SELECT name, url, title FROM links"
    ).fetchall()
    outer_links = {
        i['name']: {
            'url': i['url'],
            'title': i['title'] if i['title'] else i['url'] 
            } for i in outer_links
        }

    return dict(outer_links = outer_links)


# доступ к media
@app.route('/file/<string:filename>')
def uploaded(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



# === Главная ===
@app.route('/')
def index():
    return render_template('index.html')


# === Сохранить файл на сервер ===
def save_file(file):
    ext = file.filename[file.filename.rfind('.')+1:]
    if ext in ALLOWED_EXTENSIONS:
        file.filename = str(uuid.uuid1()) + '.' + ext
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return file.filename

# === Удалить файл ===
def delete_file(filename):
    if not filename:
        return
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)




# === Создание записки ===
@app.route('/log/create', methods = ['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        datetime = request.form['datetime']
        image = request.files['image']
        if title != "" and text != "":
            imagename = ""
            if image and image.filename != "":
                imagename = save_file(image)

            db = get_db()
            db.execute("INSERT INTO articles (title, text, date, imgpath) VALUES (?, ?, ?, ?)",
                (title, text, datetime, imagename)
            )
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
        date = request.form['date'].strip()
        hour = request.form['time']
        new_image = request.files['image']
        delimg = request.form.get('del_img')

        dt = datetime.strptime(date, "%Y-%m-%d").replace(
            hour=int(hour), tzinfo=timezone.utc
        ).timestamp()
        ts = int(dt)

        if title and text:
            imagename = article['imgpath']
            if delimg:
                delete_file(article['imgpath'])
                imagename = ""
            elif new_image and new_image.filename:
                delete_file(article['imgpath'])
                imagename = save_file(new_image)
            db.execute(
                "UPDATE articles SET title = ?, text = ?, date = ?, imgpath = ? WHERE id = ?",
                (title, text, ts, imagename, article_id)
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
        "SELECT id, imgpath FROM articles WHERE id = ?", (article_id,)
    ).fetchone()
    if article is None:
        abort(404)

    delete_file(article['imgpath'])
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


# === Функции админ панели ===

# Админ-панель
@app.route('/admin', methods=['get', 'post'])
@login_required
def admin():
    if request.method == 'POST':
        l_name = request.form['name']
        l_description = '' #request.form['desc']
        l_url = request.form['address']
        l_title = request.form['title']
        if l_name != "" and l_url != "":
            db = get_db()
            db.execute(
                "INSERT INTO links (name, description, url, title) VALUES (?, ?, ?, ?)", (l_name, l_description, l_url, l_title)
            )
            db.commit()
        return redirect(url_for('admin'))

    db = get_db()
    links = db.execute(
        "SELECT * FROM links"
    ).fetchall()
    return render_template('panel.html', links = links)


# Удалить ссылку
@app.route('/admin/dellink/<int:link_id>')
@login_required
def del_link(link_id):
    db = get_db()
    db.execute("DELETE FROM links WHERE id = ?", (link_id,))
    db.commit()

    return redirect(url_for('admin'))


# === другие страницы ===

# Статические страницы
@app.route('/pages/<path:filename>')
def pages(filename):
    return send_from_directory('pages', filename)


# Галерея
@app.route('/gallery')
def gallery():
    db = get_db()
    articles = [i for i in db.execute('SELECT imgpath, title FROM articles').fetchall() if i['imgpath'] != '']
    return render_template('gallery.html', articles = articles)

# ССылки на офф. сайты
@app.route('/helpfull-links')
def helpfull_links():
    db = get_db()
    links_drivers = db.execute('SELECT * FROM links WHERE name = "driver"').fetchall()
    links_programs = db.execute('SELECT * FROM links WHERE name = "program"').fetchall()
    
    return render_template('links.html', helpful_links = {'driver':links_drivers, 'program':links_programs})

# Minecraft сервер
@app.route('/minecraft')
def minecraft():
    return render_template('mine.html')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404