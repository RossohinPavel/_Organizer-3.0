import sqlite3


# Сортирует строки в базе данных и оптимизирует ее


def main():
    with sqlite3.connect('../../data/library.db', isolation_level=None) as connect:
        cursor = connect.cursor()

        # Получаем заголовки таблиц
        cursor.execute('SELECT * FROM sqlite_sequence')

        for table, table_len in cursor.fetchall():
            # Получаем и сортируем заголовки продуктов
            cursor.execute(f'SELECT full_name FROM {table}')

            sorted_names = sorted(x[0] for x in cursor.fetchall())

            # Обновляем данные в таблице
            # Сначало накурчиваем длинна таблицы + 1, чтобы потом начать с 1. Во избежание конфликта номеров
            cursor.executemany(f'UPDATE {table} SET id=? WHERE full_name=?', enumerate(sorted_names, start=table_len + 1))
            cursor.executemany(f'UPDATE {table} SET id=? WHERE full_name=?', enumerate(sorted_names, start=1))

            # Обновляем параметр, который следит за последовательностью
            cursor.execute('UPDATE sqlite_sequence SET seq=? WHERE name=?', (len(sorted_names), table))

        # коммитим изменения и вызываем вакум
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main()
