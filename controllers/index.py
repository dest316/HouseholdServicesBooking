from app import app
from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.index_model import get_services, get_masters_by_date, get_added_cost, get_client, add_new_orders_services, add_new_order, add_new_schedule_orders, add_new_client_if_not_exist, get_shift_id_by_master_id


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    selected_value = []
    df_service = get_services(conn)
    df_masters_by_date = None

    if request.values.get('selectedItems[]'):
        selected_value = request.args.getlist('selectedItems[]')
        session['data_form1'] = request.args.getlist('selectedItems[]')
        added_costs = []
        for item in selected_value:
            result = get_added_cost(conn, item)['summ'][0]
            if result is not None:
                added_costs.append(int(result))
            else:
                added_costs.append(0)
        session['added_costs'] = added_costs
        # print(session['data_form1'])

    elif request.values.get('selected_date') and request.values.get('selected_time'):
        session['data_form2'] = request.args.get('selected_date')
        session['awaited_time'] = request.args.get('selected_time')
        df_masters_by_date = get_masters_by_date(conn, session['data_form2'], session['awaited_time'])
    elif request.values.get('address') and request.values.get('phone_number'):
        new_client_id = add_new_client_if_not_exist(conn, request.values.get('address'), request.values.get('phone_number'), request.values.get('fio'))
        if new_client_id is None:
            new_client_id = get_client(conn, request.values.get('phone_number'), request.values.get('address'))
        new_order_id = add_new_order(conn, new_client_id, session['data_form2'])
        add_new_schedule_orders(conn, get_shift_id_by_master_id(conn, request.values.get('free_masters'), session['data_form2']).loc[0, 'shift_id'], new_order_id, session['awaited_time'])
        for item in session['data_form1']:
            add_new_orders_services(conn, int(item), new_order_id)
        session['data_form1'] = []
        session['data_form2'] = []
        session['masters'] = []
        session['added_costs'] = []
        session['awaited_time'] = []


    # вошли первый раз
    else:
        session['data_form1'] = []
        session['data_form2'] = []
        session['masters'] = []
        session['added_costs'] = []
        session['awaited_time'] = []
    html = render_template(
        'index.html',
        reader_id=session['reader_id'],
        combo_box=df_service,
        len=len,
        selected_value=selected_value,
        int=int,
        sum=sum,
        data_form1=session['data_form1'],
        selected_date=session['data_form2'],
        masters_by_date=df_masters_by_date,
        added_costs=session['added_costs']
    )
    return html
