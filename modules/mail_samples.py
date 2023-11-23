from safe_connect import SafeConnect


class MailSamples:
    __slots__ = '__s_con'

    def __init__(self) -> None:
        self.__s_con = SafeConnect('app.db')

    def get_headers(self) -> list[tuple[int, str, str]]: #type: ignore
        """Получение заголовков текстовых шаблонов"""
        with self.__s_con as sc:
            sc.cursor.execute('SELECT id, tag, name FROM Samples')
            return sorted(sc.cursor.fetchall(), key=lambda x: (x[1], x[2]))

    def get(self, sample_id: int) -> tuple[str, str, str]: #type: ignore
        """Получение тага, названия и текста шаблона"""
        with self.__s_con as sc:
            sc.cursor.execute('SELECT tag, name, data FROM Samples WHERE id=?', (sample_id, ))
            return sc.cursor.fetchone()

    def delete(self, sample_id: int) -> None: 
        """Удаление шаблона из хранилища"""
        with self.__s_con as sc:
            sc.cursor.execute('DELETE FROM Samples WHERE id=?', (sample_id, ))
            sc.connect.commit()

    def save(self, sample_id: int | None, tag: str, name: str, sample: str) -> None:
        """Сохранение текстового шаблона в бд"""
        with self.__s_con as sc:
            values = (tag, name, sample, sample_id)
            if sample_id is not None:
                sc.cursor.execute(f'UPDATE Samples SET tag=?, name=?, data=? WHERE id=?', values)
            else:
                sc.cursor.execute(f'INSERT INTO Samples (tag, name, data) VALUES (?, ?, ?)', values[:-1])
            sc.connect.commit()
