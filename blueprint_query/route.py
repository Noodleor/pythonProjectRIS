import os
from flask import Blueprint, render_template, request, current_app, session, redirect, url_for
from access import login_required, group_required
from work_with_db import select_dict
from sql_provider import SQLProvider

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')
# provider_2 = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# print(os.path.dirname(__file__))
# print(os.path.join(os.path.dirname(__file__), 'sql'))

# @blueprint_auth.route('/', methods=['GET', 'POST'])
# def authorisation():
#     if request.method == 'GET':
#         return render_template('authorisation.html')
#     else:
#         login = request.form.get('login')
#         password = request.form.get('password')
#         if not login or not password:
#             return render_template('authorisation.html')
#         else:
#             _sql = 'select * from internal_users join external_users where login="$login" and password="$password"'
#             #_sql = provider_2.get('auth.sql', login=login, password=password)
#             user = select_dict(current_app.config['db_config'], _sql)
#             print(user)
#             if user:
#                 #print(session['user_id'], session['user_group'])
#                 session['user_id'] = user[0]['user_id']
#                 session['user_group'] = user[0]['user_group']
#                 #print(session['user_id'], session['user_group'])
#                 return redirect(url_for('main_menu'))
#             else:
#                 return render_template('authorisation.html') #'Авторизация не удалась'


@blueprint_query.route('/queries')
@login_required
@group_required
def queries():
    return render_template('queries.html')


@blueprint_query.route('/full_menu')
@login_required
@group_required
def query_index1():
    tname = request.form.get('tname')
    weight = request.form.get('weight')
    price = request.form.get('price')
    _sql = provider.get('full_menu.sql', tname=tname, weight=weight, price=price)
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Вот результаты из БД'
        return render_template('dynamic_fm.html', products=products, prod_title=prod_title)


@blueprint_query.route('/order_list', methods=['GET', 'POST'])
@login_required
@group_required
def query_index2():
    if request.method == 'GET':
        return render_template('input_param_ol.html')
    else:
        idorder = request.form.get('idorder')
        _sql = provider.get('order_list.sql', idorder=idorder)
        products = select_dict(current_app.config['db_config'], _sql)
        if products:
            prod_title = 'Вот результаты из БД'
            return render_template('dynamic_ol.html', products=products, prod_title=prod_title)
        else:
            return 'Результат не найден'


@blueprint_query.route('/courier_without_delivery')
@login_required
@group_required
def query_index3():
    _sql = provider.get('courier_without_delivery.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Вот результаты из БД'
        return render_template('dynamic_cwd.html', products=products, prod_title=prod_title)


@blueprint_query.route('/courier_without_delivery_in_march_2017')
@login_required
@group_required
def query_index4():
    _sql = provider.get('courier_without_delivery_in_march_2017.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    if products:
        prod_title = 'Вот результаты из БД'
        return render_template('dynamic_cwdim2017.html', products=products, prod_title=prod_title)
