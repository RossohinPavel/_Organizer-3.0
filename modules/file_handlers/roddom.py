from os import walk as os_walk, makedirs as os_makedirs
from shutil import copy2 as sh_copy2
from re import search
from ..app_manager import AppManager


class Roddom:
    __slots__ = 'path', 'order', '__make_txt', '__img_len'
    storage = AppManager.storage

    def __init__(self, path: str, make_txt=True):
        self.__make_txt = make_txt
        self.__img_len = 0
        self.path, self.order = path.rsplit('/', 1)

    def get_calc_info(self) -> dict:
        """Получение информации о заказе"""
        dct = {'9x15': 0, '15x21': 0, '21x30': 0}
        for path, files in self.__walk_on_order():
            dct[path.split('\\')[-1]] += len(files)
        if self.__make_txt:
            with open(f'{self.path}/{self.order}/sum.txt', 'w', encoding='utf-8') as file:
                print(*(f'{k}: {v}' for k, v in dct.items()), sep='\n', file=file)
        self.__img_len = sum(dct.values())
        return dct

    def __walk_on_order(self):
        """Генераторная ф-я для пробега по файлам заказа"""
        for root in os_walk(f'{self.path}/{self.order}'):
            rel_path = root[0].removeprefix(self.path)
            if search(r'\d{1,2}x\d{2}', rel_path):
                yield rel_path, root[-1]

    def to_print(self, path):
        self.storage.pf.header.set(f'Роддом: {self.order}')
        current, maximum = 0, self.__img_len
        self.storage.pf.pb['maximum'] = maximum
        self.storage.pf.pb['value'] = 0
        for rel_path, files in self.__walk_on_order():
            new_path = f'{path}/{rel_path}'
            os_makedirs(new_path, exist_ok=True)
            for file in files:
                current += 1
                self.storage.pf.status.set(f'{current}/{maximum}: {file}')
                sh_copy2(f'{self.path}/{rel_path}/{file}', f'{new_path}/{file}')
                self.storage.pf.pb['value'] += 1
