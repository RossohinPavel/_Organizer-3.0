from sys import path as sys_path
from os import name as os_name


match os_name:
    case 'nt':
        sys_path.insert(0, __file__.rsplit('\\', maxsplit=3)[0])
    case 'posix' | _:
        sys_path.insert(0, __file__.rsplit('/', maxsplit=3)[0])


import sqlite3
from modules.data_base.library.products import *


def insert_test_rows():
    integer = ('carton_length', 'carton_height', 'cover_flap', 'cover_joint', 'dc_top_indent', 'dc_left_indent', 'dc_overlap', 'dc_break')

    with sqlite3.connect('../../data/library.db') as lib:
        cursor = lib.cursor()

        for product in (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct):
            keys = ', '.join(product._fields)
            values_req = ', '.join('?'*len(product._fields))
            values = [0 if field in integer else field for field in product._fields]
            cursor.execute(f'INSERT INTO {product.__name__} ({keys}) VALUES ({values_req})', values)
            lib.commit()


if __name__ == '__main__':
    insert_test_rows()
