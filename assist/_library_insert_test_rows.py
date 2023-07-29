import sqlite3
import os
from modules.library import Library as Lib


def insert_test_rows():
    with sqlite3.connect('../data/library.db') as lib:
        cursor = lib.cursor()
        for category in Lib.product._categories:
            keys = []
            values = []
            for k, v in Lib.product(category).__dict__.items():
                if k.startswith('_'):
                    continue
                if k == 'full_name':
                    v = f'{category}_test'
                if type(v) == tuple:
                    v = v[0]
                keys.append(f'\"{k}\"')
                values.append(f'\"{v}\"')
            keys = ', '.join(keys)
            values = ', '.join(values)
            req = f'INSERT INTO {category} ({keys}) VALUES ({values})'
            cursor.execute(req)
            lib.commit()


if __name__ == '__main__' and os.path.exists('../data/library.db'):
    insert_test_rows()
