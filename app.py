import json
from flask import Flask, redirect, url_for, render_template
from blueprint_query.route import blueprint_query
from blueprint_auth.auth import blueprint_auth
from blueprint_report.route import blueprint_report
from blueprint_busket.route import blueprint_basket
from access import session

app = Flask(__name__)
with open('db_config.json') as f:
    app.config['db_config'] = json.load(f)
with open('access.json') as f:
    app.config['access_config'] = json.load(f)

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/authorisation')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_basket, url_prefix='/order')
app.secret_key = 'KYS'


@app.route('/')
def start():
    return render_template('start.html')


@app.route('/menu')
def main_menu():
    # session['user_id'] = 0
    # session['user_group'] = 'guest'
    return render_template('main_menu.html')  # redirect(url_for('bp_query.query_index'))


@app.route('/exit')
def exit_func():
    session.clear()
    # session.pop('user.id')  # закрытие сессии пользователя
    return 'Всего хорошего'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
