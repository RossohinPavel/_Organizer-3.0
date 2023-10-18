import sqlite3



with sqlite3.connect('data/library.db') as connect:
    cursor = connect.cursor()
    cursor.execute('INSERT INTO Canvas (full_name, product_format) VALUES (?, ?)', ('test', 'test'))
