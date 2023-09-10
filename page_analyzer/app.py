import os
from flask import (
    Flask,
    render_template,
    get_flashed_messages,
    request,
    flash,
    redirect,
    url_for
)

from . import db, web_utils

app = Flask(__name__)

app.database_url = os.getenv('DATABASE_URL')
app.secret_key = os.getenv('SECRET_KEY')


def get_redirect_to_url_details_page(id):
    return redirect(url_for('get_url_details', id=id))


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.get('/urls')
def urls_show():
    dbase = db.FDataBase()
    data = dbase.get_urls_and_last_checks_data()

    return render_template('urls/index.html', data=data)


@app.post('/urls')
def post_url():
    dbase = db.FDataBase()
    url_name = request.form.get('url')
    errors = web_utils.validate_url(url_name)

    if errors:
        for error in errors:
            flash(error, 'danger')

        return render_template('index.html', url_name=url_name,
                               messages=get_flashed_messages(with_categories=True), ), 422

    url_name = web_utils.get_normalyze_url(url_name)
    url = dbase.get_url_by_url_name(url_name)

    if url:
        flash('Страница уже существует', 'info')
        id = url.id
    else:
        id = dbase.add_url(url_name)
        flash('Страница успешно добавлена', 'success')

    return get_redirect_to_url_details_page(id)


@app.get('/urls/<int:id>')
def get_url_details(id):
    dbase = db.FDataBase()
    return render_template('urls/url.html', url=dbase.get_url_by_id(id),
                           url_checks=dbase.get_url_checks_by_url_id(id),
                           messages=get_flashed_messages(with_categories=True), )


@app.post('/urls/<int:id>/checks')
def post_url_check(id):
    dbase = db.FDataBase()
    url = dbase.get_url_by_id(id)
    status_code = web_utils.get_status_code_by_url(url.name)

    if status_code and status_code < 400:
        tags_data = web_utils.get_tags_data(url.name)
        dbase.create_url_check(url, status_code, tags_data)

        flash('Страница успешно проверена', 'success')
    else:
        flash('Произошла ошибка при проверке', 'danger')

    return get_redirect_to_url_details_page(id)
