from ._safe_connect import SafeConnect


class MailSamples:
    __instance = None
    __s_con = SafeConnect('app.db')

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_headers(self) -> list:
        """Получение заголовков текстовых шаблонов"""
        with self.__s_con:
            self.__s_con.cursor.execute('SELECT id, tag, name FROM Samples')
            return sorted(self.__s_con.cursor.fetchall(), key=lambda x: x[1])

    def get_sample(self, sample_id: int) -> list:
        """Получение текста шаблоне"""
        with self.__s_con:
            self.__s_con.cursor.execute('SELECT data FROM Samples WHERE id=?', (sample_id, ))
            return self.__s_con.cursor.fetchone()[0]

    def del_sample(self, sample_id: int):
        """Удаление шаблона из хранилища"""
        with self.__s_con:
            self.__s_con.cursor.execute('DELETE FROM Samples WHERE id=?', (sample_id, ))
            self.__s_con.connect.commit()

    def save(self, sample_id: int | None, tag: str, name: str, sample: str):
        """Сохранение текстового шаблона в бд"""
        with self.__s_con:
            values = (tag, name, sample, sample_id)
            if sample_id is not None:
                self.__s_con.cursor.execute(f'UPDATE Samples SET tag=?, name=?, data=? WHERE id=?', values)
            else:
                self.__s_con.cursor.execute(f'INSERT INTO Samples (tag, name, data) VALUES (?, ?, ?)', values[:-1])
            self.__s_con.connect.commit()
