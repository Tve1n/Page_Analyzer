import os
from contextlib import contextmanager
from urllib.parse import urlparse

import psycopg2
from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for

from page_analyzer import db
from page_analyzer.validator import validate

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
def urls_list():
    with connect(DATABASE_URL) as conn:
        urls_list = db.get_all_urls(conn)
    return render_template(
            'urls.html',
            urls=urls_list
        )


@app.post('/urls')  # Добавление нового url и перенаправления на него
def url_add():
    url_name = request.form.get('url')
    errors = validate(url_name)
    if errors:
        for error in errors:
            flash(error, 'error')
        render_template(
            'index.html'
        ), 422
    url_parsed = urlparse(url_name)
    url_name = f'{url_parsed.scheme}://{url_parsed.netloc}'
    with connect(DATABASE_URL) as conn:
        url_to_check = db.get_url_by_name(conn, url_name)
        if url_to_check:
            flash("Страница уже существует", 'warning')
            return redirect(url_for('url_info', id=url_to_check[0]))
        url_id = db.create_url(conn, url_name)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('url_info', id=url_id)) 


@app.get('/urls/<int:id>')  # Получение определённого id из базы
def url_info(id):
    with connect(DATABASE_URL) as conn:
        url = db.get_url_by_id(conn, id)
        url_checks = db.get_checks_by_url_id(conn, id)
    return render_template(
        'url_id.html',
        url=url,
        checks=url_checks
    )


@app.post('/urls/<int:id>/checks')
def url_check(id):
    with connect(DATABASE_URL) as conn:
        # url = db.get_url_by_id(conn, id)
        db.create_check(conn, id)
    
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('url_info', id=id))