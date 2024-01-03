from .data_base import DataBase
from ..app_manager import AppManager
from ..mytyping import Callable


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
        - color - Цветовая палитра, которая используется в приложении
    """
    __slots__ = ()
    data_base = 'app.db'

    # Дескрипторы атрибутов
    autolog = AppManager._desc.autolog
    log_check_depth = AppManager._desc.log_check_depth
    z_disc = AppManager._desc.z_disc
    o_disc = AppManager._desc.o_disc
    t_disc = AppManager._desc.t_disc
    roddom_dir = AppManager._desc.roddom_dir
    theme = AppManager._desc.theme
    color = AppManager._desc.color

    def __init__(self) -> None:
        for name, value in self.__get_saving_values():
            setattr(self, name, value)
            eval(f'AppManager._desc.{name}.add_call(self.closure(name))')

    @DataBase.safe_connect
    def __get_saving_values(self) -> list[tuple[str, str | int]]:
        """Получаем настройки из бд при открытии программы"""
        self.cursor.execute('SELECT name, data FROM Settings')
        return self.cursor.fetchall()

    def closure(self, name: str) -> Callable[[str | int], None]:
        """Замыкание, для получения функции записи в базу данных"""
        return lambda v: self.__update_data_bese(name, v)
    
    @DataBase.safe_connect
    def __update_data_bese(self, name: str, value: str | int) -> None:
        """Обновление базы данных"""
        self.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, name))
        self.connect.commit()