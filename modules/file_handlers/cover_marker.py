import os
from re import fullmatch as re_fullmatch
from ..app_manager import AppManager


@AppManager
class CoverHandler:

    def __init__(self):
        self.cache = {}
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__

    @staticmethod
    def get_covers_from_comparison(path: str, comp: str | None) -> tuple:
        """Возвращает кортеж, В котором находятся обложки согласно совмещению"""
        target = 'Covers'
        if comp in ('Копии', 'О_О'):
            target = 'Constant'
        return tuple(f'{target}/{c}' for c in os.listdir(f'{path}/{target}') if re_fullmatch(r'cover_\d{3}\.jpg', c))


class CoverMarkerHandler(CoverHandler):
    def __call__(self, obj, **kwargs):
        for edt, prd in obj.target.items():
            src_path = f'{self.storage.stg.z_disc}/{obj.creation_date}/{obj.order}/{edt.name}'
            print(self.get_covers_from_comparison(src_path, edt.comp))
