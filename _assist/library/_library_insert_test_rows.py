import sqlite3
import os
from modules.library.products import *


def insert_test_rows():
    categories = ('Album', 'Canvas', 'Journal', 'Layflat', 'Photobook', 'Photofolder',  'Subproduct')
    with sqlite3.connect('../../data/library.db') as lib:
        cursor = lib.cursor()
        for category in categories:
            keys = []
            values = []
            for k, v in eval(f'{category}(True)').__dict__.items():
                if k == 'full_name':
                    v = f'{category}_test_2'
                if type(v) == tuple:
                    v = v[0]
                keys.append(f'\"{k}\"')
                values.append(f'\"{v}\"')
            keys = ', '.join(keys)
            values = ', '.join(values)
            req = f'INSERT INTO {category} ({keys}) VALUES ({values})'
            cursor.execute(req)
            lib.commit()


# if __name__ == '__main__' and os.path.exists('../data/library.db'):
#     insert_test_rows()
