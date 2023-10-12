from ._safe_connect import SafeConnect


class MailSamples:
    __instance = None
    __s_con = SafeConnect('mail_samples.db')

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def get_headers(self) -> list:
        """Получение заголовков текстовых шаблонов"""
        with self.__s_con:
            self.__s_con.cursor.execute('SELECT id, tag, name FROM Samples')
            return sorted(self.__s_con.cursor.fetchall(), key=lambda x: x[1])

    def get_sample(self, id: int) -> list:
        """Получение текста шаблоне"""
        with self.__s_con:
            self.__s_con.cursor.execute(f'SELECT sample FROM Samples WHERE id={id}')
            return self.__s_con.cursor.fetchone()[0]

    def del_sample(self, s_id: int):
        """Удаление шаблона из хранилища"""
        with self.__s_con:
            self.__s_con.cursor.execute(f'DELETE FROM Samples WHERE id={s_id}')
            self.__s_con.connect.commit()

    def save(self, s_id: int | None, tag: str, name: str, sample: str):
        """Сохранение текстового шаблона в бд"""
        with self.__s_con:
            if s_id is not None:
                req = f'tag=\'{tag}\', name=\'{name}\', sample=\'{sample}\''
                self.__s_con.cursor.execute(f'UPDATE Samples SET {req} WHERE id={s_id}')
            else:
                self.__s_con.cursor.execute(f'INSERT INTO Samples (tag, name, sample) VALUES (\'{tag}\', \'{name}\', \'{sample}\')')
            self.__s_con.connect.commit()
