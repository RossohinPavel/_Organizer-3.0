from typing import Callable, TypeVar


__all__ = (
    'Autolog', 
    'Log_check_depth',
    'Z_disc',
    'O_disc',
    'T_disc',
    'Roddom_dir',
    'Theme',
    'Color'
)


V = TypeVar('V')


class MainDescriptor[V]:
    """
        Класс, реализующий логику работы дескриптора.
        Помимо этого, при получении значения, вызывает
        связанные функции из _funcs.
    """

    __slots__ = '_value', '_funcs'

    def __init__(self):
        self._value: V = None   #type: ignore
        self._funcs = ()

    def __get__(self, *_) -> V:
        return self._value

    def __set__(self, _, value: V) -> None:
        self._value = value
        for func in self._funcs: func(value)

    def add_call(self, func: Callable[[V], None]) -> None:
        """Добавление функции в коллекцию вызовов"""
        self._funcs += (func, )


# Дескрипторы настроек
Autolog = MainDescriptor[int]()
Log_check_depth = MainDescriptor[int]()
Z_disc = MainDescriptor[str]()
O_disc = MainDescriptor[str]()
T_disc = MainDescriptor[str]()
Roddom_dir = MainDescriptor[str]()
Theme = MainDescriptor[str]()
Color = MainDescriptor[str]()

# Остальные дескрипторы
FileQueue = MainDescriptor[int]()
