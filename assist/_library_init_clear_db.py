import sqlite3
from old_modules.library import Library as Lib


def create_clear_db():
    with sqlite3.connect('../data/library.db') as lib:
        cursor = lib.cursor()
        product = Lib.product
        for category in product._categories:
            descr = ''
            for k, v in product(category).__dict__.items():
                if k.startswith('_'):
                    continue
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