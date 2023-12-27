from sys import path as sys_path
from os import name as os_name


match os_name:
    case 'nt':
        sys_path.insert(0, __file__.rsplit('\\', maxsplit=3)[0])
    case 'posix' | _:
        sys_path.insert(0, __file__.rsplit('/', maxsplit=3)[0])


import sqlite3
from modules.data_base.library.products import *


def create_clear_db():
    with sqlite3.connect('../../data/library.db') as lib:
        cursor = lib.cursor()

        # Создаем таблицу с псевдонимами
        cursor.execute(
            """CREATE TABLE Aliases 
            (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                alias TEXT,
                name TEXT
            )"""
        )

        for product in (Album, Canvas, Journal, Layflat, Photobook, Photofolder, Subproduct):
            req = 'id INTEGER PRIMARY KEY AUTOINCREMENT'
            for field in product._fields:
                # определение типа ячейки
                field_type = 'TEXT'
                if field in ('carton_length', 'carton_height', 'cover_flap', 'cover_joint', 
                'dc_top_indent', 'dc_left_indent', 'dc_overlap', 'dc_break'):
                    field_type = 'INTEGER'
                
                # Добавляем информацию в общий запрос
                req += f',\n{field} {field_type}'

            # Создаем таблицу
            cursor.execute(f'CREATE TABLE {product.__name__}\n({req})')


if __name__ == '__main__':
    create_clear_db()
