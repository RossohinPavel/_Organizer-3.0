import sqlite3


def create_clear_log():
    with sqlite3.connect('../data/log.db') as log:
        log.cursor().execute("""CREATE TABLE LOG (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                order_name TEXT,
                                creation_date TEXT
                                )""")


if __name__ == '__main__':
    create_clear_log()