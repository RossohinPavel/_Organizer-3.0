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
    """
    def __init__(self):
        """Чтение настроек. Вызвывается только при инициализации объекта"""
        with open('data/settings.pcl', 'rb') as file:
            self.__dict__.update(pickle.load(file))

    def __getattr__(self, item):
        if item in self.__dict__:
            return self.__dict__[item]
        raise AttributeError(f'Атрибута {item} нет в настройках')

    def __setattr__(self, key, value):
        if not isinstance(value, type(getattr(self, key))):
            raise ValueError(f'Неправильный тип устанавливаемого значения {value} для атрибута {key}')
        self.__dict__[key] = value
        self.__update_settings()

    def __str__(self):
        return f'{self.__class__.__name__}: {self.__dict__}'

    def __update_settings(self):
        """Обновление настроек. Вызывается только при обновлении сохраняемых в файл настроек."""
        with open('data/settings.pcl', 'wb') as file:
            pickle.dump(self.__dict__, file)
