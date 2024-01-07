"""
    Скрипт для 'оптимизации' базы данных.
    Сортирует строки в базе данных по имени продукции
    Сжимает неиспользуемое пространство.
"""
import sqlite3


def alias_sort(cursor):
    cursor.execute('SELECT * FROM Aliases')
    res = cursor.fetchall()
    cursor.execute('DELETE FROM Aliases')
    cursor.executemany(
        """INSERT INTO Aliases (alias, category, product_id) VALUES (?, ?, ?)""",
        sorted(res, key=lambda x: (x[1], x[0]))     #type: ignore
        )


def alias_update(cursor: sqlite3.Cursor, category: str, old_id: int, new_id: int):
    cursor.execute(
        """UPDATE Aliases SET product_id=? WHERE category=? AND product_id=?""",
        (new_id, category, old_id)
    )


def main():
    with sqlite3.connect('../../data/library.db', isolation_level=None) as connect:
        cursor = connect.cursor()

        # Сортируем псевдонимы
        alias_sort(cursor)
        
        # Получаем заголовки таблиц
        cursor.execute('SELECT * FROM sqlite_sequence')

        for table, table_len in cursor.fetchall():
            # Получаем и сортируем заголовки продуктов
            cursor.execute(f'SELECT id, name FROM {table}')
            sorted_names = sorted((list(x) for x in cursor.fetchall()), key=lambda x: x[1])

            # Присваиваем новые id продуктам и обновляем псевдонимы для них
            for new_id, product in enumerate(sorted_names, start=1):
                alias_update(cursor, table, product[0], new_id)
                product[0] = new_id

            # Обновляем данные в таблице
            # Сначало накурчиваем длинна таблицы + 1, чтобы потом начать с 1. Во избежание конфликта номеров
            cursor.executemany(
                f'UPDATE {table} SET id=? WHERE name=?', 
                enumerate((x[1] for x in sorted_names), start=table_len + 1)
            )
            # Обновляем значения
            cursor.executemany(
                f'UPDATE {table} SET id=? WHERE name=?',
                sorted_names
            )

            # Обновляем параметр, который следит за последовательностью
            cursor.execute('UPDATE sqlite_sequence SET seq=? WHERE name=?', (len(sorted_names), table))

        # коммитим изменения и вызываем вакум
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main()
