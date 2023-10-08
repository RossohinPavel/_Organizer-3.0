import sqlite3


with sqlite3.connect('../data/log.db') as connect:
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM Editions WHERE order_name=327327')
    print(cursor.fetchone())
