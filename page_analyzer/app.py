import os
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for  # flash,

# from urllib.parse import urlparse
from page_analyzer import db

# from page_analyzer.validator import validate

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@contextmanager
def connect(bd_url):
    try:
        connection = psycopg2.connect(bd_url)
        yield connection
    except Exception:
        if connection:
            connection.rollback()
        raise
    else:
        if connection:
            connection.commit()
    finally:
        if connection:
            connection.close()


@app.get('/')
def index():
    return render_template(
        'index.html'
)


@app.get('/urls')
def urls():
    with connect(DATABASE_URL) as conn:
        urls_list = db.get_all_urls(conn)
    return render_template(
            'url_id.html',
            url=urls_list
        )


@app.post('/urls')  # Добавление нового url и перенаправления на него
def url_add():
    url_name = request.form.get('url')
    with connect(DATABASE_URL) as conn:
        url_id = db.create_url(conn, url_name)
        return redirect(url_for('url_info', id=url_id)) 


@app.get('/urls/<int:id>')  # Получение определённого id из базы
def url_info(id):
    with connect(DATABASE_URL) as conn:
        url = db.get_url_by_id(conn, id)
        return render_template(
            'url_id.html',
            url=url
        )


'''
@app.get('/urls')
def urls_list():
    with conn.cursor() as curs:
        urls = db.get_all_urls(curs)
'''