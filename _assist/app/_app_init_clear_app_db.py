import sqlite3


def create_clear_app_db():
    with sqlite3.connect('../../data/app.db') as connect:
        cursor = connect.cursor()
        cursor.execute("CREATE TABLE Images (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, data BLOB)")
        cursor.execute('CREATE TABLE Samples (id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT, name TEXT, data TEXT)')
        cursor.execute('CREATE TABLE Settings (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, data INT)')


def fill_images_table():
    with open('D:/app.png', 'rb') as file:
        app_blob = file.read()
    with open('D:/btn.png', 'rb') as file:
        btn_blob = file.read()
    with sqlite3.connect('../../data/app.db') as connect:
        cursor = connect.cursor()
        values = (('app_ico', app_blob), ('question_ico', btn_blob))
        cursor.executemany('INSERT INTO Images (name, data) VALUES (?, ?)', values)
        connect.commit()


def fill_settings_table():
    with sqlite3.connect('../../data/app.db') as connect:
        cursor = connect.cursor()
        values = (('autolog', 0), ('log_check_depth', 5), ('z_disc', ''), ('o_disc', ''), ('t_disc', ''), ('roddom_dir', ''))
        cursor.executemany('INSERT INTO Settings (name, data) VALUES (?, ?)', values)
        connect.commit()


if __name__ == '__main__':
    create_clear_app_db()
    fill_images_table()
    fill_settings_table()
    pass
