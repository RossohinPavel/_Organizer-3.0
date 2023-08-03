__all__ = ('Settings', )
import pickle


class Settings:
    """Предоставляет доступ к настройкам и сохраняет их текущие значения:
    - is_alive - Используется вторым потоком для проверки существования основного
    - autolog - Инициализация записи лога файлов в автоматическом режиме
    - log_check_depth - Глубина проверки лога в днях (папках)
    - orders_complete_check - При автоматическом логе, проверка целостности заказа (копирование файлов)
    - z_disc - Ссылка на серверный диск, куда загружаются заказы
    - o_disc - Ссылка на серверный диск, откуда происходит печать заказов
    - t_disc - Ссылка на серверный диск цифрового отдела и операторов фотопечати
    """
    __slots__ = ()
    __instance = None
    __stored = {'autolog': False, 'log_check_depth': 1, 'orders_complete_check': False,
                'z_disc': '', 'o_disc': '', 't_disc': ''}
    __operational = {'is_alive': True}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__read_settings()
        return cls.__instance

    @classmethod
    def __read_settings(cls):
        """Чтение настроек. Вызвывается только при инициализации объекта"""
        with open('data/settings.pcl', 'rb') as file:
            cls.__stored.update(pickle.load(file))

    @classmethod
    def __update_settings(cls):
        """Обновление настроек. Вызывается только при обновлении сохраняемых в файл настроек."""
        with open('data/settings.pcl', 'wb') as file:
            pickle.dump(cls.__stored, file)

    def __getattr__(self, item):
        if item in self.__stored:
            return self.__stored[item]
        if item in self.__operational:
            return self.__operational[item]
        raise AttributeError(f'Атрибута {item} нет в настройках')

    def __setattr__(self, key, value):
        if not isinstance(value, type(getattr(self, key))):
            raise ValueError(f'Неправильный тип устанавливаемого значения {value} для атрибута {key}')
        if key in self.__operational:
            self.__operational[key] = value
        if key in self.__stored:
            self.__stored[key] = value
            self.__update_settings()

    def __str__(self):
        return f'{self.__class__.__name__}:\n_Stored - {self.__stored}\n_Operational - {self.__operational}'
