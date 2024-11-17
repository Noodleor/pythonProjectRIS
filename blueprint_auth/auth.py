from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from work_with_db import select_dict
from sql_provider import SQLProvider

import os

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def authorisation():
    if request.method == 'GET':
        return render_template('authorisation.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        # if not login or not password:
        #     return render_template('authorisation.html', error='Некорректный ввод')
        _sql = provider.get('auth.sql', login=login, password=password)
        user = select_dict(current_app.config['db_config'], _sql)
        print(user)
        if user is None:
            return render_template('authorisation.html', error='Неверный логин или пароль')
        else:
            # print(session['user_id'], session['user_group'])
            session['user_id'] = user[0]['user_id']
            session['user_group'] = user[0]['user_group']
            # print(session['user_id'], session['user_group'])
            return redirect(url_for('main_menu'))
            # return render_template('authorisation.html') #'Авторизация не удалась'


@blueprint_auth.route('/lk')
def lk_index():
    if 'user_id' in session:
        user_group = session.get('user_group')
    return render_template('lk.html', user_group=user_group)
