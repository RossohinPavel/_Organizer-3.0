import sqlite3


def create_clear_log():
    with sqlite3.connect('../data/log.db') as log:
        log.cursor().execute("""CREATE TABLE Orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                creation_date TEXT,
                                path TEXT,
                                customer_name TEXT,
                                customer_address TEXT,
                                price INT
                                )""")
        log.cursor().execute("""CREATE TABLE Editions (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        order_name TEXT,
                                        name TEXT,
                                        covers INT,
                                        pages INT,
                                        ccount TEXT,
                                        comp TEXT,
                                        price INT
                                        )""")
        log.cursor().execute("""CREATE TABLE Photos (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        order_name TEXT,
                                        name TEXT,
                                        count INT
                                        )""")


if __name__ == '__main__':
    create_clear_log()