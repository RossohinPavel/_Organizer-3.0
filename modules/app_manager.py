__all__ = ('AppManagerR', 'AppManagerW', 'AppManager')


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
        if not isinstance(obj, AppManagerW | AppManagerR):
            raise AttributeError(f'{obj} не является объектом-наследником классов AppManager')
        self.__dict__[attr_name] = obj

    def __contains__(self, item):
        return item in self.__dict__


class AppManagerR:
    """Абстрактный класс, предостовляющий наследникам доступ к хранилищу модулей приложения по переменной app_m"""
    app_m = Storage()


class AppManagerW:
    """Абстрактный класс, при создании объекта записывает его в хранилище. По факту - реализует моносостояние."""
    def __new__(cls, *args, **kwargs):
        storage = Storage()
        if cls.__name__ not in storage:
            setattr(storage, cls.__name__, super().__new__(cls))
        return getattr(storage, cls.__name__)


class AppManager(AppManagerR, AppManagerW):
    """Абстрактный класс, предостовляющий наследникам как доступ к хранилищу модулей приложения, так и записывающий
    модуль в это хранилище"""
    pass
