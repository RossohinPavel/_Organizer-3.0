from os import listdir
from re import fullmatch
from typing import Iterator


# Паттерны для проверки модулем re
DAY_PATTERN = r'\d{4}(-\d{2}){2}'
ORDER_PATTERN = r'\d{6}'


def orders_grabber_iterator(path: str) -> Iterator[tuple[str, str]]:
    """Итератор по номерам заказов и датам их создания. Возвращает значения в виде кортежа:\t
    (<дата создания>, <имя заказа>)\nЗначения возвращаются в обратном порядке. От новых к старым."""
    for day in reversed(listdir(path)):
        if fullmatch(DAY_PATTERN, day):
            for order in reversed(listdir(f'{path}/{day}')):
                if fullmatch(ORDER_PATTERN, order):
                    yield day, order


# class EditionGrabberIterator:
#     """Предоставляет итератор по именам каталогов и именам файлов в тираже.
#     Возвращает значения в виде кортежа, (<имя каталога>, итератор по именам файлов)"""
#     __slots__ = 'path', 'mode'
#     sample = r'(cover|\d{3})_{1,2}(\d{3}|-?\d+_pcs){1,2}\.jpg'

#     def __init__(self, path: str, *mode: tuple[str] | str):
#         """
#         :param path: Путь до искомого тиража.
#         :param mode: Указание того, какие папки будут захвачены.
#         Literal['Exemplar' - Захват папок экземпляров,
#                 'Constant' - Захват папки Constant
#                 'Covers' - Захват папки Covers
#                 'Variable' - Захват папки Variable]
#         """
#         self.path = path
#         self.mode = mode

#     def __iter__(self):
#         yield from self.__grab()

#     def __grab(self) -> (str, (str, )):
#         """Основная ф-я для захвата"""
#         ex = 'Exemplar' in self.mode
#         for catalog in listdir(self.path):
            # c_path = f'{self.path}/{catalog}'
            # if ex and fullmatch(r'\d{3}(-\d+_pcs)?', catalog) or catalog in self.mode:
                # yield catalog, (name for name in listdir(f'{c_path}') if fullmatch(self.sample, name))