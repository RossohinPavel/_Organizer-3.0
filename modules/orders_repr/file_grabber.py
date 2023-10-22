from os import listdir
from re import fullmatch


class EditionGrabberIterator:
    """Предоставляет итератор по именам каталогов и именам файлов в тираже.
    Возвращает значения в виде кортежа, (<имя каталога>, итератор по именам файлов).
    В папки экземпляры захватывает только развороты.
    В папки Constant и Covers захватывает все подходящие изображения."""
    __slots__ = 'path'

    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        yield from self.__grab()

    def __grab(self):
        for catalog in listdir(self.path):
            c_path = f'{self.path}/{catalog}'
            if fullmatch(r'\d{3}(-\d+_pcs)?', catalog):
                yield catalog, (x for x in listdir(f'{c_path}') if fullmatch(r'(cover|\d{3}_)_\d{3}(-\d+_pcs)?.jpg', x))
            if catalog == 'Constant':
                yield catalog, (x for x in listdir(f'{c_path}') if fullmatch(r'(cover|\d{3})_\d+_pcs.jpg', x))
