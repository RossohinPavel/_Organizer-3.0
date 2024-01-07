import sqlite3


def create_clear_app_db():
    with sqlite3.connect('../../data/mail_samples.db') as connect:
        cursor = connect.cursor()
        cursor.execute(
            """CREATE TABLE Samples (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                tag TEXT, 
                name TEXT, 
                data TEXT
            )"""
        )


if __name__ == '__main__':
    create_clear_app_db()
