import sqlite3


def create_clear_log():
    with sqlite3.connect('../data/log.db') as log:
        log.cursor().execute("""CREATE TABLE Orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                creation_date TEXT,
                                customer_name TEXT,
                                customer_address TEXT,
                                price REAL
                                )""")
        log.cursor().execute("""CREATE TABLE Editions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        order_name TEXT,
                                        name TEXT,
                                        covers INT,
                                        pages INT,
                                        ccount TEXT,
                                        comp TEXT
                                        )""")
        log.cursor().execute("""CREATE TABLE Photos (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        order_name TEXT,
                                        name TEXT,
                                        count INT
                                        )""")


if __name__ == '__main__':
    create_clear_log()