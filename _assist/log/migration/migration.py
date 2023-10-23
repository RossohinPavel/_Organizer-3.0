import sqlite3


# Осуществляет миграцию записей из старой базы данных в новую.
# Принудительно сортирует записи по имени заказа


def main():
    with sqlite3.connect('../../../data/log.db') as current_con, sqlite3.connect('log_21_10_2023.db') as old_con:
        current_cursor = current_con.cursor()
        old_cursor = old_con.cursor()
        old_cursor.execute('SELECT name, creation_date, customer_name, customer_address, price FROM Orders')
        current_cursor.executemany("""INSERT INTO Orders (name, creation_date, customer_name, customer_address, price)
                                      VALUES (?, ?, ?, ?, ?)""", sorted(old_cursor.fetchall(), key=lambda x: x[0]))
        old_cursor.execute('SELECT order_name, name, covers, pages, ccount, comp FROM Editions')
        current_cursor.executemany("""INSERT INTO Editions (order_name, name, covers, pages, ccount, comp) 
                                      VALUES (?, ?, ?, ?, ?, ?)""", sorted(old_cursor.fetchall(), key=lambda x: x[0]))
        old_cursor.execute('SELECT order_name, name, count FROM Photos')
        current_cursor.executemany("""INSERT INTO Photos (order_name, name, count) 
                                      VALUES (?, ?, ?)""", sorted(old_cursor.fetchall(), key=lambda x: x[0]))

#
# if __name__ == '__main__':
#     main()
