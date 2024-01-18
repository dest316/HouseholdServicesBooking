import sqlite3

conn = sqlite3.connect('../service.sqlite')

cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS components (
        component_id INTEGER PRIMARY KEY AUTOINCREMENT,
        component_name TEXT NOT NULL,
        component_price INTEGER NOT NULL
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS services (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_type TEXT NOT NULL,
        service_price INTEGER NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_personal_data TEXT,
        client_address TEXT NOT NULL,
        client_phone_number TEXT
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS masters (
        master_id INTEGER PRIMARY KEY AUTOINCREMENT,
        master_personal_data TEXT NOT NULL
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        shift_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        master_id INTEGER NOT NULL,
        FOREIGN KEY (master_id) REFERENCES masters (master_id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        is_finished INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (client_id) REFERENCES clients (client_id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS services_components (
        service_components_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        component_id INTEGER NOT NULL,
        amount INTEGER NOT NULL,
        FOREIGN KEY (service_id) REFERENCES services (service_id),
        FOREIGN KEY (component_id) REFERENCES components (component_id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS orders_services (
        orders_services_id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        FOREIGN KEY (service_id) REFERENCES services (service_id),
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS schedule_orders (
        schedule_orders_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shift_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        order_datetime TEXT,
        FOREIGN KEY (shift_id) REFERENCES schedule (shift_id),
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    )
''')
