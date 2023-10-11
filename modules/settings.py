import pickle
from .app_manager import AppManager

__all__ = ('Settings', )


class Settings(AppManager):
    """Предоставляет доступ к настройкам и сохраняет их текущие значения:
    - autolog - Инициализация записи лога файлов в автоматическом режиме
    - log_check_depth - Глубина проверки лога в днях (папках)
    - z_disc - Ссылка на серверный диск, куда загружаются заказы
    - o_disc - Ссылка на серверный диск, откуда происходит печать заказов
    - t_disc - Ссылка на серверный диск цифрового отдела и операторов фотопечати
    - roddom_dir - Ссылка на папку, где хранятся заказы Роддома
    """
    _alias = 'stg'

    def __init__(self):
        """Чтение настроек. Вызвывается только при инициализации объекта"""
        with open('data/settings.pcl', 'rb') as file:
            for key, value in pickle.load(file).items():
                self.__dict__[key] = None
                setattr(self, key, value)

    def __setattr__(self, key, value):
        """Обновляем файл настроек при изменении атрибутов объекта"""
        if key not in self.__dict__:
            raise AttributeError(f'Атрибута {key} нет в настройках')
        if key == 'autolog':    # Когда меняется атрибут autolog, инициализируем фоновую функцию трекера
            self.app_m.tr.ot.init_auto(value)
            if not value:
                self.app_m.txt_vars.orders_trk.set('Выключен')
        self.__dict__[key] = value
        with open('data/settings.pcl', 'wb') as file:
            pickle.dump(self.__dict__, file)
