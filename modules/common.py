import re
from modules.appmanager import AppManagerW


__all__ = ('Constants', 'MyDict')


class Constants(AppManagerW):
    """Класс, который содержит в себе постоянные, использующиеся для проверки в различных частях приложения"""
    __day = r'\d{4}-\d{2}-\d{2}'
    __order = r'\d{6}'

    @classmethod
    def check_day(cls, value):
        """Проверка переданной строки (value) на соответсвие паттерну дня"""
        return re.fullmatch(cls.__day, value)

    @classmethod
    def check_order(cls, value):
        """Проверка переданной строки (value) на соответсвие паттерну заказа"""
        return re.fullmatch(cls.__order, value)


class MyDict(dict):
    __getattribute__ = dict.get
    __setattr__ = dict.__setitem__
