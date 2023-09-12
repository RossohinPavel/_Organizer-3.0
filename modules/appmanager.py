__all__ = ('AppManager', 'AppManagerW')


class Storage:
    """Объект - хранилище для модулей программы"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, attr_name, obj):
        if not isinstance(obj, AppManager | dict):
            raise AttributeError(f'{obj} не является объектом-наследником класса AppManager или dict')
        self.__dict__[attr_name] = obj

    def __contains__(self, item):
        return item in self.__dict__


class AppManager:
    """Абстрактный класс, предостовляющий наследникам доступ к хранилищу модулей приложения"""
    app_m = Storage()


class AppManagerW(AppManager):
    """Абстрактный класс, предостовляющий наследникам доступ к хранилищу модулей приложения. При создании объекта
    записывает его в хранилище. По факту - реализует моносостояние."""
    def __new__(cls, *args, **kwargs):
        if cls.__name__ not in cls.app_m:
            setattr(cls.app_m, cls.__name__, super().__new__(cls))
        return getattr(cls.app_m, cls.__name__)
