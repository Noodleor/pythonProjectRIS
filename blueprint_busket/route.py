import os
from flask import Blueprint, render_template, request, current_app, redirect, session, url_for
from sql_provider import SQLProvider
from work_with_db import select_dict, save_order_with_list
import random as rnd

# from authentication_blueprint.access import login_required, group_required

blueprint_basket = Blueprint('bp_order', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


# print(os.path.dirname(__file__))
# print(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_basket.route('/', methods=['GET', 'POST'])
def order_index():
    if request.method == 'GET':
        _sql = provider.get('all_items.sql')
        products = select_dict(current_app.config['db_config'], _sql)
        current_basket = session.get('basket', {})
        return render_template('baskets_orders_list.html', items=products, basket=current_basket)
    else:
        product_id = request.form.get('id_dishm')
        _sql = provider.get('check.sql', product_id=product_id)
        item = select_dict(current_app.config['db_config'], _sql)
        print('iiiiiiiii', _sql, item)
        add_to_basket(product_id, item[0])
        return redirect(url_for('bp_order.order_index'))  # new http query type get


@blueprint_basket.route('/order_created', methods=['GET'])
def save_order():
    user_id = rnd.randint(1, 1000)
    current_basket = session.get('basket', {})
    if current_basket is not None:
        print(current_basket)
        order_id = save_order_with_list(current_app.config['db_config'], user_id, current_basket, provider)
        session.pop('basket')
        return render_template('order_created.html', order_id=order_id, products=current_basket,
                               total=count_final_sum(current_basket))
    # return "Заказ создан"


def add_to_basket(prod_id, item):
    session.permanent = True
    if 'basket' not in session:
        session['basket'] = {}
    if prod_id not in session['basket']:
        session['basket'][prod_id] = {'name': item['name'], 'price': item['price'], 'quantity': 1}
    else:
        session['basket'][prod_id]['quantity'] += 1
    current_basket = session.get('basket', {})
    _sql = provider.get('all_items.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    return render_template('baskets_orders_list.html', items=products, basket=current_basket)


@blueprint_basket.route('/clear', methods=['GET'])
def clear_basket():
    session['basket'].clear()
    _sql = provider.get('all_items.sql')
    products = select_dict(current_app.config['db_config'], _sql)
    current_basket = session.get('basket', {})
    return redirect(url_for('bp_order.order_index'))
    # return render_template('baskets_orders_list.html', items=products, basket=current_basket)


def count_final_sum(basket):
    final_sum = 0
    for product in basket.values():
        final_sum += product['price'] * product['quantity']
    return final_sum
