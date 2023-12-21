from .data_base import DataBase


class Settings(DataBase):
    """
        Предоставляет доступ к настройкам и сохраняет их текущие значения:
        - autolog - Инициализация записи лога файлов в автоматическом режиме
        - log_check_depth - Глубина проверки лога в днях (папках)
        - z_disc - Ссылка на серверный диск, куда загружаются заказы
        - o_disc - Ссылка на серверный диск, откуда происходит печать заказов
        - t_disc - Ссылка на серверный диск цифрового отдела и операторов фотопечати
        - roddom_dir - Ссылка на папку, где хранятся заказы Роддома
        - theme - Название темы, которая используется в приложении
    """
    __slots__ = 'autolog', 'log_check_depth', 'z_disc', 'o_disc', 't_disc', 'roddom_dir', 'theme', 'color'

    data_base = 'app.db'

    def __init__(self) -> None:
        # Типы данных настроек
        self.autolog: int
        self.log_check_depth: int
        self.z_disc: str
        self.o_disc: str
        self.t_disc: str
        self.roddom_dir: str
        self.theme: str
        self.color: str
        self.__get_saving_values()

    @DataBase.safe_connect
    def __get_saving_values(self) -> None:
        """Получаем настройки из бд при открытии программы"""
        self.cursor.execute('SELECT name, data FROM Settings')
        for name, value in self.cursor.fetchall():
            super().__setattr__(name, value)

    def __setattr__(self, name: str, value: int | str) -> None:
        """Обновляет атрибуты на объекте, запускает связанные с ними функции и обновляет базу данных"""
        super().__setattr__(name, value)
        self.__update_db(name, value)

    @DataBase.safe_connect
    def __update_db(self, name: str, value: int | str) -> None:
        """Обновление базы данных"""
        self.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, name))
        self.connect.commit()
