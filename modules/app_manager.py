__all__ = ('AppManager', )


class Group:
    """Класс-контейнер."""
    def __init__(self, group_name: str):
        self._group_name = group_name

    def __repr__(self):
        return f'<{self._group_name}>: {", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.__dict__.items() if k != "_group_name")}'


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

    def __contains__(self, item):
        return self.__getattr__(item) is not None

    def __repr__(self):
        return f'Storage: <{repr(self.__dict__)}>'


class AppManager:
    """Класс-декоратор для сборки основных модулей программы в storage и предостовления к ним доступа. Если аргумент
    write=True, то объект этого класса будет записан в storage. Для подобных объектов реализовано моносостояние."""
    __slots__ = '__write'
    storage = Storage()

    def __new__(cls, write: object | bool) -> object:
        """Фильтруем аргументы. Если передан класс, то возвращаем объект класса AppManager с аргументом write=False."""
        if isinstance(write, type):
            return cls(False)(write)
        return super().__new__(cls)

    def __init__(self, write: object | bool):
        self.__write = write

    def __call__(self, type_obj: type = None) -> type:
        """Наполняем передаваемый класс атрибутом класса storage и, если write=True, подменяем функцию __new__"""
        type_obj.storage = self.storage
        if self.__write:
            setattr(type_obj, '__new__', self.__new_decorator(getattr(type_obj, '__new__')))
        return type_obj

    @classmethod
    def __new_decorator(cls, new_func: callable) -> callable:
        """Декоратор функции __new__. Реализует моносостояние и записывает объект класса в storage"""
        def wrapper(instance, *args, **kwargs):
            if instance.__name__ not in cls.storage:
                name = f'{instance.__name__}={getattr(instance, "_alias", "")}'
                setattr(cls.storage, name, new_func(instance))
            return getattr(cls.storage, instance.__name__)
        wrapper.__name__, wrapper.__doc__ = new_func.__name__, new_func.__doc__
        return wrapper

    @classmethod
    def create_group(cls, group_name: str, alias: str = '') -> Group:
        """Создает в Storage группу (Group) и возвращает ее"""
        group = Group(group_name)
        setattr(cls.storage, f'{group_name}={alias}', group)
        return group
