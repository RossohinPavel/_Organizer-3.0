import sqlite3


def create_clear_log():
    with sqlite3.connect('../data/mail_samples.db') as db:
        db.cursor().execute("""CREATE TABLE Samples (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                tag TEXT,
                                name TEXT,
                                sample TEXT
                                )""")


if __name__ == '__main__':
    create_clear_log()