from .data_base import DataBase


class MailSamples(DataBase):
    __slots__ = ()

    data_base = 'app.db'

    @DataBase.safe_connect
    def create(self, tag: str, name: str, text: str) -> None:
        """Сохранение нового текстового шаблона в бд"""
        self.cursor.execute(f'INSERT INTO Samples (tag, name, data) VALUES (?, ?, ?)', (tag, name, text))
        self.connect.commit()

    @DataBase.safe_connect
    def get_headers(self) -> list[tuple[int, str, str]]: #type: ignore
        """Получение заголовков текстовых шаблонов"""
        self.cursor.execute('SELECT id, tag, name FROM Samples')
        return sorted(self.cursor.fetchall(), key=lambda x: (x[1], x[2]))

    @DataBase.safe_connect
    def get(self, sample_id: int) -> tuple[str, str, str]: #type: ignore
        """Получение тага, названия и текста шаблона"""
        self.cursor.execute('SELECT tag, name, data FROM Samples WHERE id=?', (sample_id, ))
        return self.cursor.fetchone()

    @DataBase.safe_connect
    def delete(self, sample_id: int) -> None: 
        """Удаление шаблона из хранилища"""
        self.cursor.execute('DELETE FROM Samples WHERE id=?', (sample_id, ))
        self.connect.commit()
    
    @DataBase.safe_connect
    def update(self, sample_id: int, tag: str, name: str, text: str) -> None:
        """Обновление текстового шаблона в бд"""
        self.cursor.execute(f'UPDATE Samples SET tag=?, name=?, data=? WHERE id=?', (tag, name, text, sample_id))
        self.connect.commit()
