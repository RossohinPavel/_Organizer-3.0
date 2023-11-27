import sqlite3


def main(db_path: str) -> None:
    with sqlite3.connect(db_path, isolation_level=None) as connect:
        cursor = connect.cursor()
        # Получаем все строки и сортируем их
        cursor.execute('SELECT tag, name, data FROM Samples')
        rows = cursor.fetchall()
        rows.sort()
        # очищаем таблицу
        cursor.execute('DELETE FROM Samples')
        # обновляем sqlite_sequence, которая автоматически присваивает id
        cursor.execute('UPDATE sqlite_sequence SET seq=? WHERE name=?', (0, 'Samples'))
        # Записываем заново данные в таблицу
        cursor.executemany('INSERT INTO Samples (tag, name, data) VALUES (?, ?, ?)', rows)
        # Сохраняем изменения и выполняем VACUUM для сжатия неиспользуемого места таблицы
        connect.commit()
        cursor.execute(f'VACUUM')


if __name__ == '__main__':
    main('../../data/app.db')
