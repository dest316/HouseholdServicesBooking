import pandas


def get_services(conn):
    return pandas.read_sql(
        '''
        SELECT * FROM services
        ''', conn)


def get_masters_by_date(conn, date):
    return pandas.read_sql(f''' 
     SELECT *
FROM masters m
JOIN schedule s ON m.master_id = s.master_id
LEFT JOIN schedule_orders so ON s.shift_id = so.shift_id
WHERE date = '{date}'
GROUP BY s.shift_id
HAVING COUNT(*) <= 4
;''', conn)


def get_added_cost(conn, service_id):
    return pandas.read_sql(
        f'''
        SELECT SUM(component_price * amount) as summ FROM services 
        JOIN services_components USING (service_id) 
        JOIN components USING (component_id)
        WHERE service_id='{service_id}'
        ''', conn
    )


def get_book_reader(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql('''
 WITH get_authors( book_id, authors_name)
 AS(
 SELECT book_id, GROUP_CONCAT(author_name)
 FROM author JOIN book_author USING(author_id)
 GROUP BY book_id
 )
 SELECT title AS Название, authors_name AS Авторы,
 borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
 book_reader_id
 FROM
 reader
 JOIN book_reader USING(reader_id)
 JOIN book USING(book_id)
 JOIN get_authors USING(book_id)
 WHERE reader.reader_id = :id
 ORDER BY 3
 ''', conn, params={"id": reader_id})


# для обработки данных о новом читателе
def get_new_reader(conn, new_reader):
    cur = conn.cursor()
    # добавить нового читателя в базу
    cur.execute(f'INSERT INTO reader (reader_name) VALUES ({new_reader})')
    return cur.lastrowid


# для обработки данных о взятой книге
def borrow_book(conn, book_id, reader_id):
    cur = conn.cursor()
    # добавить взятую книгу (book_id) читателю (reader_id) в таблицу book_reader
    # указать текущую дату как дату выдачи книги
    # уменьшить количество экземпляров взятой книги
    return True
