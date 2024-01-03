from typing import Callable, Self, TypeVar, Generic


T = TypeVar('T')


class DescriptorConstructor(Generic[T]):
    """
        Класс, реализующий логику работы дескриптора.
        Помимо этого, при получении значения, вызывает
        связанные функции из _funcs.
    """

    __slots__ = '_value', '_funcs'

    def __init__(self):
        self._value: T = None   #type: ignore
        self._funcs = ()

    def __get__(self, *_) -> T:
        return self._value

    def __set__(self, _, value: T) -> None:
        self._value = value
        for func in self._funcs: func(value)

    def add_call(self, func: Callable[[T], None]) -> None:
        """Добавление функции в коллекцию вызовов"""
        self._funcs += (func, )


class Descriptors:
    """Объект, который содержит в себе все дескрипторы"""

    __instance = None

    __slots__ = (
        'autolog',
        'log_check_depth',
        'z_disc',
        'o_disc',
        't_disc',
        'roddom_dir',
        'theme',
        'color'
    )

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        # Дескрипторы настроек
        self.autolog = DescriptorConstructor[int]()
        self.log_check_depth = DescriptorConstructor[int]()
        self.z_disc = DescriptorConstructor[str]()
        self.o_disc = DescriptorConstructor[str]()
        self.t_disc = DescriptorConstructor[str]()
        self.roddom_dir = DescriptorConstructor[str]()
        self.theme = DescriptorConstructor[str]()
        self.color = DescriptorConstructor[str]()
