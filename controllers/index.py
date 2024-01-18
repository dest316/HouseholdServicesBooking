from app import app
from flask import render_template, request, session
#import sqlite3
from utils import get_db_connection
from models.index_model import get_services, get_masters_by_date, get_added_cost


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()
    selected_value = []
    df_service = get_services(conn)
    df_masters_by_date = None

    if request.values.get('selectedItems[]'):
        selected_value = request.args.getlist('selectedItems[]')
        session['data_form1'] = request.args.getlist('selectedItems[]')
        print(get_added_cost(conn, '3')['summ'][0])
        added_costs = []
        for item in selected_value:
            result = get_added_cost(conn, item)['summ'][0]
            if result is not None:
                added_costs.append(int(result))
            else:
                added_costs.append(0)
        session['added_costs'] = added_costs
        # print(session['data_form1'])

    elif request.values.get('selected_date'):
        session['data_form2'] = request.args.get('selected_date')
        df_masters_by_date = get_masters_by_date(conn, session['data_form2'])
        #print(session['data_form2'])

    # вошли первый раз
    else:
        session['reader_id'] = 1
        session['data_form1'] = []
        session['data_form2'] = []
        session['masters'] = []
        session['added_costs'] = []
    # print(session['data_form1'])
    # df_book_reader = get_book_reader(conn, session['reader_id'])
# выводим форму
    # print(df_masters_by_date)
    print(session['added_costs'])
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
