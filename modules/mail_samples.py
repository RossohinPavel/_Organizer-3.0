from .db_contextmanager import SafeConnect


class MailSamples:
    __s_con = SafeConnect('mail_samples.db')

    def get_headers(self) -> list:
        """Получение заголовков текстовых шаблонов"""
        with self.__s_con:
            self.__s_con.cursor.execute('SELECT tag, name FROM Samples')
            return sorted(f'{tag} - {name}' for tag, name in self.__s_con.cursor.fetchall())

    def get_sample(self, tag_and_name: str) -> list:
        """Получение текста шаблоне в виде списка, элементы которого разбиты по разделителю ?%"""
        with self.__s_con:
            tag, name = tag_and_name.split(' - ', maxsplit=1)
            self.__s_con.cursor.execute(f'SELECT sample FROM Samples WHERE tag=\'{tag}\' AND name=\'{name}\'')
            return self.__s_con.cursor.fetchone()[0].split('?%')
