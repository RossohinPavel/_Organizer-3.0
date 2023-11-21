from typing import Any, Self, Type, Callable


class IDescriptor:
    """Дескриптор для хранения значений переменных, и вызова добавленных функций"""
    __slots__ = '_value', '_callbacks'

    def __init__(self) -> None:
        self._value: Any = None
        self._callbacks = ()

    def __set__(self, instance, value: Any) -> None:
        """Присвоенное значение будет передано в каждую ф-ю из спискка _callbacks"""
        self._value = value
        for call in self._callbacks:
            call(value)

    def __get__(self, instance, instance_class):
        return self._value
    
    def add_callback(self, callable: Type[Callable[[Any, Any], Any]]) -> None:
        """Добавляет функцию в список вызовов"""
        self._callbacks += (callable, )


class Test:
    def some_func(self, value):
        print(self, value)


class Test1:
    def some_func(self, value):
        print(self, value)


class Storage:
    attr = IDescriptor()
    attr.add_callback(Test.some_func)
    attr.add_callback(Test1.some_func)


t1 = Test()
t2 = Test1()

s = Storage()
s.attr = True

print(s.attr)