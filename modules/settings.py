from .app_manager import AppManager
from ._safe_connect import SafeConnect

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
    storage = AppManager.storage
    __new__ = AppManager.write_to_storage('stg')
    __slots__ = 'autolog', 'log_check_depth', 'z_disc', 'o_disc', 't_disc', 'roddom_dir', '__init'
    __s_con = SafeConnect('app.db')

    def __init__(self):
        """Чтение настроек. Вызвывается только при инициализации объекта"""
        self.__init = False
        with self.__s_con as conn:
            conn.cursor.execute('SELECT name, data FROM Images')    # Получение картинок, использующихся в приложении
            self.storage.mw.set_app_img(conn.cursor.fetchall())
            conn.cursor.execute('SELECT name, data FROM Settings')
            for name, value in conn.cursor.fetchall():
                setattr(self, name, value)
        self.__init = True

    def __setattr__(self, key, value):
        """Обновляем файл настроек при изменении атрибутов объекта"""
        super().__setattr__(key, value)
        if key == 'autolog':
            self.storage.tr.ot.init_auto(value)
            if not value:
                self.storage.txt_vars.orders_trk.set('Выключен')
        self.__update_settings(key, value)

    def __update_settings(self, key, value):
        if self.__init and key in self.__slots__[:-1]:
            with self.__s_con as conn:
                conn.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, key))
                conn.connect.commit()
