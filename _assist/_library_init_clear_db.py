import sqlite3
from modules.library.products import product_base
from modules.library.properties import Blank


def create_clear_db():
    with sqlite3.connect('../data/library.db') as lib:
        cursor = lib.cursor()
        for obj in (Blank(x).create_blank() for x in product_base):
            descr = ''
            for k in obj.__slots__:
                v = getattr(obj, k)
                if type(v) == tuple:
                    v = v[0]
                row = f'{k} {"INTEGER" if type(v) == int else "TEXT"}'
                if descr:
                    row = ',\n' + row
                descr += row
            # print(descr)
            sql_req = f'CREATE TABLE {obj.category}\n(id INTEGER PRIMARY KEY AUTOINCREMENT,\n{descr})'
            cursor.execute(sql_req)


# if __name__ == '__main__':
#     create_clear_db()
