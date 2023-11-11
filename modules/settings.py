from typing import Self, Any
from ._safe_connect import SafeConnect
from ._appmanager import AppManager

__all__ = ('Settings', )


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
    __instance = None
    __scon = SafeConnect('app.db')

    def __new__(cls) -> Self:
        if cls.__instance is None:
            obj = super().__new__(cls)
            with cls.__scon as sc:
                # Получение картинок, использующихся в приложении
                sc.cursor.execute('SELECT name, data FROM Images') 
                AppManager.mw.set_app_img(sc.cursor.fetchall())
                # Получение и установка на объект остальных настроек
                sc.cursor.execute('SELECT name, data FROM Settings')
                for name, value in sc.cursor.fetchall():
                    setattr(obj, name, value)
            cls.__instance = obj
        return cls.__instance

    def __setattr__(self, key: str, value: Any) -> None:
        """Обновляем файл настроек при изменении атрибутов объекта"""
        super().__setattr__(key, value)
        # if key == 'autolog':
        #     AppManager.storage.tr.ot.init_auto(value)
        #     if not value:
        #         AppManager.storage.txt_vars.orders_trk.set('Выключен')
        if self.__instance:
            self.__update_settings(key, value)

    def __update_settings(self, key: str, value: Any) -> None:
        """Обновляет настройки в базе данных если прилождение инициализировано"""
        with self.__scon as sc:
            sc.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, key))
            sc.connect.commit()
