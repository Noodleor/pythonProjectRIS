from flask import Blueprint, render_template, request, current_app, redirect, url_for
from work_with_db import select_dict, call_proc
import os
from sql_provider import SQLProvider

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/')
def report():
    return render_template('choose.html')


@blueprint_report.route('/create', methods=['GET', 'POST'])
def report_create():
    if request.method == 'GET':
        return render_template('otchet_in.html')
    else:
        year = request.form.get('in_date')
        month = request.form.get('out_date')
        try:
            year = int(year)
            month = int(month)
        except ValueError:
            return render_template('otchet_in.html', error='Некорректный ввод')
        _sql = provider.get('check_rep.sql', date_start=year, date_end=month)
        cost = select_dict(current_app.config['db_config'], _sql)
        print(cost)
        if cost is not None:
            prod_title = 'Данный отчет уже существует'
            # return render_template('dynamic_otchet.html', products=cost, prod_title=prod_title)
            return redirect(url_for('bp_report.check_reports'))
        else:
            cost = call_proc(current_app.config['db_config'], 'calc_sum', year, month)
            _sql = provider.get("print_last.sql", date_start=year, date_end=month)
            res = select_dict(current_app.config['db_config'], _sql)
            prod_title = "Отчет успешно создан"
            print(_sql, res)
            if cost is None or res is None:
                return render_template('otchet_in.html', error='Продажи за указанный период не найдены')
            else:
                return render_template('dynamic_otchet.html', products=res, prod_title=prod_title)


@blueprint_report.route('/check', methods=['GET', 'POST'])
def check_reports():
    _sql = provider.get("date_get.sql")
    res = select_dict(current_app.config['db_config'], _sql)
    print(res)
    if res is not None:
        prod_title = 'существующие отчеты'
        return render_template('dynamic_otchet.html', products=res, prod_title=prod_title)
    else:
        return redirect(url_for('bp_report.report_create'))
