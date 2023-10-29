from ._handler import *


class CanvasHandler(Handler):
    __slots__ = 'proxy', 'cache', '__name__'
    grabber_mode = 'Exemplar',

    def get_processing_frame_header(self) -> str:
        return f'Обработка холстов в заказе {self.proxy.name}'

    def get_total_sum_of_images(self) -> int:
        return sum(len(tuple(x.covers_from_ex_iter())) for x in self.proxy.files)

    def handler_run(self, product, file_grabber, kwargs):
        # Формируем путь, куда будут сохранятся обложки и создаем соответствующую папку.
        save_place = f'{self.destination}/{self.middle_path}'
        os_makedirs(save_place, exist_ok=True)
        # Создаем в kwargs дополнительный атрибут для подсчета холстов
        if 'canvas_count' not in kwargs:
            kwargs['canvas_count'] = 0
        # Получаем генератор для итерации
        for ex, cover_name, ex_len in file_grabber.covers_from_ex_iter():
            # Выводим строку статуса обработки
            self.storage.pf.status.set(f'{self.storage.pf.pb["value"] + 1}/{self.storage.pf.pb["maximum"]} {cover_name} -- {kwargs["edt_name"]}')
            # Считываем изображение холста.
            with Image.open(f'{self.source}/{self.middle_path}/{kwargs["edt_name"]}/{ex}/{cover_name}') as canvas_img:
                canvas_img.load()
            # Создаем draw объект на его онове и заполняем 3 см по периметру белым
            draw_obj = ImageDraw.Draw(canvas_img)
            draw_obj.rectangle((0, 0, canvas_img.width, canvas_img.height), outline='white', width=355)
            # Подрезаем изображение, если опция обработчика активна
            quality = 'keep'
            if kwargs['handler_option']:
                canvas_img = canvas_img.crop(box=(119, 119, canvas_img.width - 119, canvas_img.height - 119))
                quality = 100
            # Сохраняем изображение
            kwargs['canvas_count'] += 1
            cover_name = f'{kwargs["order"]}_{kwargs["canvas_count"]} холст {product.product_format} натяжка в короб.jpg'
            canvas_img.save(f'{save_place}/{cover_name}', quality=quality, dpi=(300, 300))
            self.storage.pf.pb["value"] += 1
