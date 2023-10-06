__all__ = ('AppManagerR', 'AppManagerW', 'AppManager')


class Storage:
    """Объект - хранилище для модулей программы"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __getattr__(self, item):
        for key, value in self.__dict__.items():
            if key.startswith(item) or key.endswith(item):
                return value

    def __setattr__(self, attr_name, obj):
        if not isinstance(obj, AppManagerW | AppManagerR):
            raise AttributeError(f'{obj} не является объектом-наследником классов AppManager')
        self.__dict__[attr_name] = obj

    def __contains__(self, item):
        return self.__getattr__(item) is not None


class AppManagerR:
    """Абстрактный класс, предостовляющий наследникам доступ к хранилищу модулей приложения по переменной app_m"""
    app_m = Storage()


class AppManagerW:
    """Абстрактный класс, при создании объекта записывает его в хранилище. Реализует моносостояние.
    Можно использовать как контейнер, чтобы сгруппировать некие присвоенные атрибуты"""
    _alias = ''  # псевдоним, который может использовать объект.

    def __new__(cls, *args, **kwargs):
        storage = Storage()
        name = kwargs.get('group_name', cls.__name__)
        if name not in storage:
            if name == 'AppManagerW':
                raise TypeError('Не передан аргумент group_name')
            setattr(storage, f'{name}={kwargs.get("alias", cls._alias)}', super().__new__(cls))
        return getattr(storage, name)


class AppManager(AppManagerR, AppManagerW):
    """Абстрактный класс, предостовляющий наследникам как доступ к хранилищу модулей приложения, так и записывающий
    модуль в это хранилище"""
    pass
