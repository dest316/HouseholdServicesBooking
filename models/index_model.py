import pandas


def get_services(conn):
    return pandas.read_sql(
        '''
        SELECT * FROM services
        ''', conn)


def get_masters_by_date(conn, date, time):
    return pandas.read_sql(f'''
    WITH temp AS (
     SELECT *
FROM masters m
JOIN schedule s ON m.master_id = s.master_id
LEFT JOIN schedule_orders so ON s.shift_id = so.shift_id
WHERE date = '{date}'
GROUP BY s.shift_id
HAVING COUNT(*) <= 4
)
SELECT * FROM temp
WHERE order_datetime <> '{time}' OR order_datetime IS NULL
;''', conn)


def add_new_client_if_not_exist(conn, address, phone_number, fio=None):
    cur = conn.cursor()
    cur.execute(f'''
    INSERT INTO clients (client_phone_number, client_address, client_personal_data)
    SELECT '{phone_number}', '{address}', '{fio}'
    WHERE NOT EXISTS (
    SELECT 1
    FROM clients
    WHERE client_phone_number = '{phone_number}' AND client_address = '{address}'
    )
''')
    conn.commit()
    return cur.lastrowid


def get_client(conn, phone_number, address):
    return pandas.read_sql(
        f'''
        SELECT * FROM clients WHERE phone_number = '{phone_number}' AND address = '{address}';
        ''', conn
    )


def add_new_order(conn, client_id, order_date):
    cur = conn.cursor()
    cur.execute(f'''
    INSERT INTO orders (client_id, order_date, is_finished)
    values ({client_id}, '{order_date}', 0)
''')
    conn.commit()
    return cur.lastrowid


def get_shift_id_by_master_id(conn, master_id, date):
    return pandas.read_sql(
        f'''
    SELECT shift_id FROM schedule WHERE master_id = {master_id} AND date = '{date}'
''', conn
    )

def add_new_schedule_orders(conn, shift_id, order_id, order_time):
    cur = conn.cursor()
    cur.execute(f'''
    INSERT INTO schedule_orders (shift_id, order_id, order_datetime)
    values ({shift_id}, {order_id}, '{order_time}')
''')
    conn.commit()
    return cur.lastrowid


def add_new_orders_services(conn, service_id, order_id):
    cur = conn.cursor()
    cur.execute(f'''
    INSERT INTO orders_services (service_id, order_id)
    values ({service_id}, {order_id})
''')
    conn.commit()
    return cur.lastrowid


def get_added_cost(conn, service_id):
    return pandas.read_sql(
        f'''
        SELECT SUM(component_price * amount) as summ FROM services 
        JOIN services_components USING (service_id) 
        JOIN components USING (component_id)
        WHERE service_id='{service_id}'
        ''', conn
    )


