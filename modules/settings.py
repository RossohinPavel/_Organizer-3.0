from typing import Any
from ._safe_connect import SafeConnect
from ._appmanager import AppManager


class Settings:
    """Предоставляет доступ к настройкам и сохраняет их текущие значения:
    - autolog - Инициализация записи лога файлов в автоматическом режиме
    - log_check_depth - Глубина проверки лога в днях (папках)
    - z_disc - Ссылка на серверный диск, куда загружаются заказы
    - o_disc - Ссылка на серверный диск, откуда происходит печать заказов
    - t_disc - Ссылка на серверный диск цифрового отдела и операторов фотопечати
    - roddom_dir - Ссылка на папку, где хранятся заказы Роддома
    """
    __slots__ = 'autolog', 'log_check_depth', 'z_disc', 'o_disc', 't_disc', 'roddom_dir'
    __scon = SafeConnect('app.db')  # Для удобства, вынесем эти атрибуты в атрибуты класса
    __is_init = False

    def __init__(self) -> None:
        self.autolog: int
        self.log_check_depth: int
        self.z_disc: str
        self.o_disc: str
        self.t_disc: str
        self.roddom_dir: str
        self.__set_start_settings_data()
        Settings.__is_init = True
    
    def __setattr__(self, __name: str, __value: Any) -> None:
        """Обновляет атрибуты на объекте, запускает связанные с ними функции и обновляет базу данных"""
        super().__setattr__(__name, __value)
        match __name:
            case 'autolog': AppManager.ot.init_auto(__value)
        self.__update_db(__name, __value)
    
    def __set_start_settings_data(self) -> None:
        """Получение настроек из бд при открытии программы и установки их на obj"""
        with self.__scon as sc:
            sc.cursor.execute('SELECT name, data FROM Images')      # Получение картинок, использующихся в приложении
            AppManager.mw.set_app_img(sc.cursor.fetchall())
            sc.cursor.execute('SELECT name, data FROM Settings')    # Получение и установка на объект остальных настроек
            for name, value in sc.cursor.fetchall():
                setattr(self, name, value)
    
    def __update_db(self, __name: str, __value: Any):
        """Замыкание, для обновления базы данных"""
        if self.__is_init:
            with self.__scon as sc:             # Обновляем данные в бд
                sc.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (__value, __name))
                sc.connect.commit()
