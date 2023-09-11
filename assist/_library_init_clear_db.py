import sqlite3
from modules.library.productgen import ProductGenerator as PG


def create_clear_db():
    with sqlite3.connect('../data/library.db') as lib:
        cursor = lib.cursor()
        for category in PG.get_categories():
            descr = ''
            for k, v in PG(category, True).__dict__.items():
                print(k, v)
                if type(v) == tuple:
                    v = v[0]
                row = f'{k} {"INTEGER" if type(v) == int else "TEXT"}'
                if descr:
                    row = ',\n' + row
                descr += row
            sql_req = f'CREATE TABLE {category}\n(id INTEGER PRIMARY KEY AUTOINCREMENT,\n{descr})'
            cursor.execute(sql_req)


if __name__ == '__main__':
    create_clear_db()
