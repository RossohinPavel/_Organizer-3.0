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
    """Класс-декоратор. """
    storage = Storage()

    @classmethod
    def write_to_storage(cls, alias='') -> callable:
        """Замена ф-ии __new__ в декорируемом классе. записывает Объект в Storage и возвращает его.
        Реализует моносостояние"""
        def wrapper(instance, *args, **kwargs):
            if instance.__name__ not in cls.storage:
                setattr(cls.storage, f'{instance.__name__}={alias}', object.__new__(instance))
            return getattr(cls.storage, instance.__name__)
        return wrapper

    @classmethod
    def create_group(cls, group_name: str, alias: str = '') -> Group:
        """Создает в Storage группу (Group) и возвращает ее"""
        group = Group(group_name)
        setattr(cls.storage, f'{group_name}={alias}', group)
        return group
