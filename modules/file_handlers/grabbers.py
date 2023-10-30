from os import listdir
from re import fullmatch


class OrdersGrabberIterator:
    """Итератор по номерам заказов и датам их создания.
    Возвращает значения в виде кортежа:
    (<дата создания>, <имя заказа>)
    Значения возвращаются в обратном порядке.
    От новых к старым."""
    __slots__ = 'path'

    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        yield from self.__grab()

    def __grab(self) -> (str, str):
        for day in reversed(listdir(self.path)):
            if fullmatch(r'\d{4}(-\d{2}){2}', day):
                for order in reversed(listdir(f'{self.path}/{day}')):
                    if fullmatch(r'\d{6}', order):
                        yield day, order


class EditionGrabberIterator:
    """Предоставляет итератор по именам каталогов и именам файлов в тираже.
    Возвращает значения в виде кортежа, (<имя каталога>, итератор по именам файлов)"""
    __slots__ = 'path', 'mode'
    sample = r'(cover|\d{3})_{1,2}(\d{3}|-?\d+_pcs){1,2}\.jpg'

    def __init__(self, path: str, *mode: tuple[str] | str):
        """
        :param path: Путь до искомого тиража.
        :param mode: Указание того, какие папки будут захвачены.
        Literal['Exemplar' - Захват папок экземпляров,
                'Constant' - Захват папки Constant
                'Covers' - Захват папки Covers
                'Variable' - Захват папки Variable]
        """
        self.path = path
        self.mode = mode

    def __iter__(self):
        yield from self.__grab()

    def __grab(self) -> (str, (str, )):
        """Основная ф-я для захвата"""
        ex = 'Exemplar' in self.mode
        for catalog in listdir(self.path):
            c_path = f'{self.path}/{catalog}'
            if ex and fullmatch(r'\d{3}(-\d+_pcs)?', catalog) or catalog in self.mode:
                yield catalog, (name for name in listdir(f'{c_path}') if fullmatch(self.sample, name))


class EditionGrabber:
    """Предостовляет различные функции для выборки изображений из тиража"""
    __slots__ = 'edition'

    def __init__(self, path: str, grabber_mode: tuple):
        self.edition = {name: tuple(imgs) for name, imgs in EditionGrabberIterator(path, *grabber_mode)}

    def covers_from_ex_iter(self):
        """Предоставляет генератор для итерации по обложкам из папок экземпляров.
        Возвращает имя экземпляра, имя обложки и количетсво разворотов в экземпляре"""
        for ex, images in self.edition.items():
            if fullmatch(r'\d{3}(-\d+_pcs)?', ex):
                for cover in reversed(images):
                    if cover.startswith('cover'):
                        yield ex, cover, len(images) - 1
                        break

    def cover_from_constant_iter(self):
        """Предоставляет генератор для итерации по постоянным обложкам.
        Возвращает Constant, имя обложки и наибольшее количество разворотов в экземпляре"""
        count = 0
        for ex, images in self.edition.items():
            if fullmatch(r'\d{3}(-\d+_pcs)?', ex):
                len_ex = len(images) - 1
                if len_ex > count:
                    count = len_ex
            if ex == 'Constant':
                for cover in reversed(images):
                    if cover.startswith('cover'):
                        yield ex, cover, count
                        break

    def pages_from_ex_iter(self, constant=False, cover_included=False):
        """Предрставляет генератор для итерации по разворотам экземпляра.
        Возвращает имя экземпляра и генератор для итерации по именам разворотов.
        Если constant=True, то итерация обрывается после выдачи 1 результата, так как развороты постоянные"""
        for ex, images in self.edition.items():
            if fullmatch(r'\d{3}(-\d+_pcs)?', ex):
                yield ex, (x for x in images if not x.startswith('cover') or cover_included)
                if constant:
                    break

    def images_from_constant_iter(self, cover_included=False):
        if 'Constant' in self.edition:
            yield from (x for x in self.edition['Constant'] if not x.startswith('cover') or cover_included)
