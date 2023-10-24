from ._handler import Handler
from os import makedirs as os_makedirs
from PIL import Image, ImageDraw, ImageFont
from time import sleep


class CoverMarkerHandler(Handler):
    __slots__ = 'proxy', 'cache', '__name__', '__doc__'

    def get_processing_frame_header(self) -> str:
        return f'Разметка обложек в заказе {self.proxy.name}'

    def get_total_sum_of_images(self) -> int:
        count = 0
        for i, f_g in enumerate(self.proxy.files):
            if self.proxy.content[i].comp in ('Копии', 'О_О', None):
                count += 1
            else:
                count += len(tuple(f_g.variable_cover_iter()))
        return count

    def run(self):
        # Получаем ссылки на диск-источник и диск, с которого идет печать.
        z_disc, o_disc  = self.storage.stg.z_disc, self.storage.stg.o_disc
        # Формируем промежуточный путь, который на этих дисках одинаковый.
        middle_path = f'{self.proxy.creation_date}/{self.proxy.name}'
        # Итерируемся по файловым объектам.
        for i, f_g in enumerate(self.proxy.files):
            # Получаем имя тиража и тип его совмещения. Эта информация будет использована в ходе дальнейшей обработки
            edt_name, comp = self.proxy.content[i].name, self.proxy.content[i].comp
            # Формируем путь, куда будут сохранятся обложки и создаем соответствующую папку.
            save_place = f'{o_disc}/{middle_path}/{edt_name}/{"Constant" if comp in ("Копии", "О_О") else "Covers"}'
            os_makedirs(save_place, exist_ok=True)
            # Получаем настройки продукта. Значения, которые указаны в мм, переводим в пиксельные.
            cover_type = self.proxy.products[i].cover_type
            clapan = self.mm_to_pixel(self.proxy.products[i].cover_clapan)
            carton_len = self.mm_to_pixel(self.proxy.products[i].carton_length)
            joint = self.mm_to_pixel(self.proxy.products[i].cover_joint)
            # Получаем генератор для итерации по обложкам исходя из типа совмещения
            cover_iter = f_g.constant_cover_iter if comp in ('Копии', 'О_О') else f_g.variable_cover_iter
            for ex, cover_name, ex_len in cover_iter():
                # Выводим строку статуса обработки
                self.storage.pf.status.set(f'{self.storage.pf.pb["value"] + 1}/{self.storage.pf.pb["maximum"]} {cover_name} -- {edt_name}')
                # Считываем длинну и высоту обложки, на основе которой будет размечаться задняя часть.
                with Image.open(f'{z_disc}/{middle_path}/{edt_name}/{ex}/{cover_name}') as cover_img:
                    cover_size = cover_img.width, cover_img.height
                # Создаем новый объект изображения на основе полученной ширины и высоты
                back = Image.new("RGB", cover_size, 'white')
                back_draw = ImageDraw.Draw(back)
                # Пропускаем объект через функции для обработки
                self.mark_carton(back_draw, cover_size, clapan, carton_len)
                self.mark_spine(back_draw, cover_type, cover_size, clapan, carton_len, joint)
                # if self.cache.get('handler_option'):
                #     self.paste_backprint()
                # Сохраняем изображение
                back.save(f'{save_place}/{cover_name[:-4]}_1.jpg', quality=100, dpi=(300, 300))
                self.storage.pf.pb["value"] += 1

    @staticmethod
    def mark_carton(back_draw, cover_size: tuple[int, int], clapan: int, carton_len: int):
        """Разметка картонок для задней части обложки"""
        color = '#000000'
        back_draw.rectangle((clapan, clapan, clapan + carton_len, cover_size[1] - clapan), outline=color)
        back_draw.rectangle((cover_size[0] - clapan, clapan, cover_size[0] - clapan - carton_len, cover_size[1] - clapan), outline=color)

    @staticmethod
    def mark_spine(back_draw, cover_type: str, cover_size: tuple[int, int], clapan: int, carton_len: int, joint: int):
        """Разметка корешка для задней части обложки"""
        main = clapan + carton_len
        if cover_type == 'Книга':
            main = main + joint
        back_draw.rectangle((main, clapan, cover_size[0] - main, cover_size[1] - clapan), outline='#000000')
        if cover_type == 'Книга':
            back_draw.rectangle((main, clapan + 99, cover_size[0] - main, cover_size[1] - clapan - 99), fill='#FFFFFF')

    @staticmethod
    def paste_backprint(back_draw, cover_size: tuple[int, int], clapan: int):
        pass