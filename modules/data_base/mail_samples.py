from .safe_connect import SafeConnect


class MailSamples:
    __slots__ = '__s_con'

    def __init__(self) -> None:
        self.__s_con = SafeConnect('app.db')
    
    def create(self, tag: str, name: str, text: str) -> None:
        """Сохранение нового текстового шаблона в бд"""
        with self.__s_con as sc:
            sc.cursor.execute(f'INSERT INTO Samples (tag, name, data) VALUES (?, ?, ?)', (tag, name, text))
            sc.connect.commit()

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
    
    def update(self, sample_id: int, tag: str, name: str, text: str) -> None:
        """Обновление текстового шаблона в бд"""
        with self.__s_con as sc:
            sc.cursor.execute(f'UPDATE Samples SET tag=?, name=?, data=? WHERE id=?', (tag, name, text, sample_id))
            sc.connect.commit()
