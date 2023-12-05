from typing import Any
from safe_connect import SafeConnect
from appmanager import AppManager


class Settings:
    """Предоставляет доступ к настройкам и сохраняет их текущие значения:
    - autolog - Инициализация записи лога файлов в автоматическом режиме
    - log_check_depth - Глубина проверки лога в днях (папках)
    - z_disc - Ссылка на серверный диск, куда загружаются заказы
    - o_disc - Ссылка на серверный диск, откуда происходит печать заказов
    - t_disc - Ссылка на серверный диск цифрового отдела и операторов фотопечати
    - roddom_dir - Ссылка на папку, где хранятся заказы Роддома
    """
    __slots__ = 'autolog', 'log_check_depth', 'z_disc', 'o_disc', 't_disc', 'roddom_dir', 'theme'
    __scon = SafeConnect('app.db')  

    def __init__(self) -> None:
        # Типы данных настроек
        self.autolog: int
        self.log_check_depth: int
        self.z_disc: str
        self.o_disc: str
        self.t_disc: str
        self.roddom_dir: str
        self.theme: str
        # Получаем настройки из бд при открытии программы
        with self.__scon as sc:
            sc.cursor.execute('SELECT name, data FROM Settings')
            for name, value in sc.cursor.fetchall():
                super().__setattr__(name, value)
                # self.__update_bound_modules(name, value)
    
    @property
    def app_ico(self) -> Any:
        """Получение иконки использующейся в приложении"""
        with self.__scon as sc:
            sc.cursor.execute('SELECT data FROM Images')
            return sc.cursor.fetchone()[0]
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Обновляет атрибуты на объекте, запускает связанные с ними функции и обновляет базу данных"""
        super().__setattr__(name, value)
        self.__update_db(name, value)
        # self.__update_bound_modules(name, value)

    def __update_bound_modules(self, name: str, value: Any) -> None:
        """Обновляет связанные модули в зависимости от полученных значенимй"""
        match name:
            case 'autolog': AppManager.ot.init_auto(value)
    
    def __update_db(self, name: str, value: Any):
        """Обновление базы данных"""
        with self.__scon as sc:             # Обновляем данные в бд
            sc.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, name))
            sc.connect.commit()
