from ._handler import Handler
from os import makedirs as os_makedirs
from PIL import Image, ImageDraw


class CanvasHandler(Handler):
    __slots__ = 'proxy', 'cache', '__name__'

    def get_processing_frame_header(self) -> str:
        return f'Обработка холстов в заказе {self.proxy.name}'

    def get_total_sum_of_images(self) -> int:
        res = sum(len(tuple(x.variable_cover_iter())) for x in self.proxy.files)
        print(res)
        return res

    def run(self):
        input()