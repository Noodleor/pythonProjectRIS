from DBcm import DBContextManager
from datetime import datetime


def select_dict(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql)
            products = cursor.fetchall()
            if products:
                schema = [item[0] for item in cursor.description]
                products_dict = []
                for product in products:
                    products_dict.append(dict(zip(schema, product)))
                return products_dict
            else:
                return None


def call_proc(dbconfig: dict, proc_name: str, *args):
    with DBContextManager(dbconfig) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []
        for arg in args:
            param_list.append(arg)
        res = cursor.callproc(proc_name, param_list)
        return res


def save_order_with_list(config, user_id, current_basket, provider):
    with DBContextManager(config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не найден')
        else:
            now = datetime.now()
            sql_date = now.strftime("%Y-%m-%d")
            sql_time = now.strftime("%H:%M:%S")
            sql_query = f"insert into user_orders (user_id, order_date, order_time) values ({user_id}, '{sql_date}', '{sql_time}')"
            print(sql_query)
            cursor.execute(sql_query)
            latest_order_id = cursor.lastrowid
            sql_query = "SELECT LAST_INSERT_ID();"
            if cursor.execute(sql_query):
                for key in current_basket.keys():
                    sql_query = f"insert into order_list (order_id, product_id, amount) values ({latest_order_id}, {key}, {current_basket[key]['amount']})"
                    print(sql_query)
                    cursor.execute(sql_query)
