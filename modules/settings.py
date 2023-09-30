import pickle
from modules.app_manager import AppManagerW

__all__ = ('Settings', )


class Settings(AppManagerW):
    """Предоставляет доступ к настройкам и сохраняет их текущие значения:
    - autolog - Инициализация записи лога файлов в автоматическом режиме
    - log_check_depth - Глубина проверки лога в днях (папках)
    - autofile - Инициализация проверки целостности файлов в заказах
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
                setattr(self, key, value)

    def __setattr__(self, key, value):
        if key == 'autolog' and value:
            print('Вызов каких-то методов для автолога')
        if key == 'autofile' and value:
            print('Вызов каких-то методов для автофала')
        self.__dict__[key] = value
        with open('data/settings.pcl', 'wb') as file:
            pickle.dump(self.__dict__, file)
