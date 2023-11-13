from typing import Self, Any
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
    __instance = None
    __scon = SafeConnect('app.db')

    def __new__(cls) -> Self:
        """Создание объекта Settings. Помимо этого, подтягивает из бд настройки и устанавливает их на объект"""
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__set_start_settings_data()
        return cls.__instance
    
    @classmethod
    def __set_start_settings_data(cls):
        """Получение настроек из бд при открытии программы и установки их на obj"""
        with cls.__scon as sc:
            sc.cursor.execute('SELECT name, data FROM Images')      # Получение картинок, использующихся в приложении
            AppManager.mw.set_app_img(sc.cursor.fetchall())
            sc.cursor.execute('SELECT name, data FROM Settings')    # Получение и установка на объект остальных настроек
            for name, value in sc.cursor.fetchall():
                super(cls, cls.__instance).__setattr__(name, value) #type: ignore

    def __setattr__(self, key: str, value: Any) -> None:
        """Обновляем файл настроек при изменении атрибутов объекта"""
        super().__setattr__(key, value)     # Делегируем установку атрибутов
        with self.__scon as sc:             # Обновляем данные в бд
            sc.cursor.execute('UPDATE Settings SET data=? WHERE name=?', (value, key))
            sc.connect.commit()
        # if key == 'autolog':                # Дополнительнеы действия
        #     AppManager.storage.tr.ot.init_auto(value)
        #     if not value:
        #         AppManager.storage.txt_vars.orders_trk.set('Выключен')
