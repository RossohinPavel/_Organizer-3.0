from os import listdir
from re import fullmatch


class GrabberIterator:
    """База для наследования остальных итераторов"""
    __slots__ = 'path'

    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        yield from self._grab()

    def _grab(self):
        """Абстрактная ф-я для захвата имен папок или файлов"""
        raise Exception('Ф-я _grab должна быть переопределена')


class OrdersGrabberIterator(GrabberIterator):
    """Итератор по номерам заказов и датам их создания.
    Возвращает значения в виде кортежа:
    (<дата создания>, <имя заказа>)
    Значения возвращаются в обратном порядке.
    От новых к старым."""
    __slots__ = 'path'

    def _grab(self) -> (str, str):
        for day in reversed(listdir(self.path)):
            if fullmatch(r'\d{4}(-\d{2}){2}', day):
                for order in reversed(listdir(f'{self.path}/{day}')):
                    if fullmatch(r'\d{6}', order):
                        yield day, order


class EditionGrabberIterator(GrabberIterator):
    """Предоставляет итератор по именам каталогов и именам файлов в тираже.
    Возвращает значения в виде кортежа, (<имя каталога>, итератор по именам файлов).
    Захватывает все изображения из папок экземпляров и Constant"""
    __slots__ = 'path'

    def _grab(self) -> (str, (str, )):
        for catalog in listdir(self.path):
            c_path = f'{self.path}/{catalog}'
            if fullmatch(r'\d{3}(-\d+_pcs)?', catalog):
                yield catalog, (x for x in listdir(f'{c_path}') if fullmatch(r'(cover|\d{3}_)_\d{3}(-\d+_pcs)?.jpg', x))
            if catalog == 'Constant':
                yield catalog, (x for x in listdir(f'{c_path}') if fullmatch(r'(cover|\d{3})_\d+_pcs.jpg', x))


class EditionGrabber:
    """Предостовляет различные функции для выборки изображений из тиража"""
    __slots__ = 'edition'

    def __init__(self, path: str):
        self.edition = {name: tuple(imgs) for name, imgs in EditionGrabberIterator(path)}

    def variable_cover_iter(self):
        """Предоставляет генератор для итерации по индивидуальным обложкам
        Возвращает имя экземпляра, имя обложки и количетсво разворотов в экземпляре"""
        for ex, images in self.edition.items():
            if ex == 'Constant':
                continue
            for cover in reversed(images):
                if cover.startswith('cover'):
                    yield ex, cover, len(images) - 1
                    break

    def constant_cover_iter(self):
        """Предоставляет генератор для итерации по постоянным обложкам.
        Возвращает имя экземпляра, она же папка Constnt, имя обложки и наибольшее количество разворотов в экземпляре"""
        count = 0
        for ex, images in self.edition.items():
            len_ex = len(images) - 1
            if len_ex > count:
                count = len_ex
            if ex == 'Constant':
                for cover in reversed(images):
                    if cover.startswith('cover'):
                        yield ex, cover, count
                        break