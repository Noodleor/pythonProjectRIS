from functools import wraps
from flask import session, current_app, request, render_template, redirect, url_for

from work_with_db import select_dict


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        return 'Вам необходимо авторизироваться'

    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            user_group = session.get('user_group')
            if user_group:
                access = current_app.config['access_config']
                user_target = request.blueprint
                if user_group in access and user_target in access[user_group]:
                    return func(*args, **kwargs)
                else:
                    return 'У вас нет доступа к этому функционалу'
            else:
                return 'Только для внутренних пользователей'
        else:
            return 'Вам необходимо авторизоваться'

    return wrapper

# def authorisation():
#     if request.method == 'GET':
#         return render_template('authorisation.html')
#     else:
#         login = request.form.get('login')
#         password = request.form.get('password')
#         if not (login and password):
#             print("111")
#             return exit(0)
#         else:
#             _sql = "select * from authorisation where login=$login and password=$password"
#             user = select_dict(current_app.config['db_config'], _sql)
#             session['user_id'] = user['user_id']
#             session['user_group'] = user['user_group']
#             return redirect(url_for('main_menu'))
