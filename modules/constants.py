import re


class Constants:
    """Класс, который содержит в себе постоянные, использующиеся для проверки в различных частях приложения"""
    __day = r'\d{4}-\d{2}-\d{2}'

    @classmethod
    def check_day(cls, value):
        """Проверка переданной строки (value) на соответсвие паттерну дня"""
        return re.fullmatch(cls.__day, value)
