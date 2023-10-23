import sqlite3


# Сортирует строки в базе данных и оптимизирует ее

def run():
    with sqlite3.connect('../../data/library.db', isolation_level=None) as connect:
        cursor = connect.cursor()
        cursor.execute('SELECT name FROM sqlite_sequence')
        tables = tuple(x[0] for x in cursor.fetchall())
        for table_name in tables:
            cursor.execute(f'SELECT id, full_name FROM {table_name}')
            rows = cursor.fetchall()
            for i, v in rows:
                cursor.execute(f'UPDATE {table_name} SET id=? WHERE full_name=?', (i + 99999, v))
            for i, v in enumerate(sorted(rows, key=lambda x: x[-1]), 1):
                cursor.execute(f'UPDATE {table_name} SET id=? WHERE full_name=?', (i, v[1]))
            cursor.execute('UPDATE sqlite_sequence SET seq=? WHERE name=?', (len(rows), table_name))
        connect.commit()
        cursor.execute(f'VACUUM')


# if __name__ == '__main__':
#     run()
