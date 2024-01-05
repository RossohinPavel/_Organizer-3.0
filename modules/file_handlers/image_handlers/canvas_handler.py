from ._handler import *


class CanvasHandler(Handler):
    __slots__ = ()
    grabber_mode = 'Exemplar',

    def get_handler_header(self, order_name: str) -> str:
        return f'Обработка холстов в заказе {order_name}'
    
    def get_total_sum_of_images(self) -> int:
        return sum(len(tuple(x.covers_from_ex())) for x in self.files if x)

    def handler_run(self, edition: Edition, product: Product, file_grabber: EditionGrabber) -> None:
        # Формируем путь, куда будут сохранятся обложки и создаем соответствующую папку.
        os_makedirs(self.destination, exist_ok=True)

        # Получаем генератор для итерации
        for ex, cover_name, _ in file_grabber.covers_from_ex():
            # Выводим строку статуса обработки
            AppManager.pf.filebar.step(cover_name)

            # Считываем изображение холста.
            with Image.open(f'{self.source}/{edition.name}/{ex}/{cover_name}') as canvas_img:
                canvas_img.load()

            # Создаем draw объект на его онове и заполняем 3 см по периметру белым
            draw_obj = ImageDraw.Draw(canvas_img)
            draw_obj.rectangle((0, 0, canvas_img.width, canvas_img.height), outline='white', width=355)

            # Переменная со значением качества
            quality = 'keep'

            # Подрезаем изображение, если опция обработчика активна
            if self.option:
                cropped = canvas_img.crop(box=(119, 119, canvas_img.width - 119, canvas_img.height - 119))
                canvas_img.close()
                canvas_img = cropped

                # Обновляем качество, так как кропнутое изображение со значением keep не сохранить
                quality = 100

            # Формируем имя холста
            name = f'{self.order_name} холст {product.format} натяжка в короб'

            # По необходимости формируем уникальные имена и добавляем имя в self.assist
            while True:
                if name in self.assist:
                    name = name + '_'
                else:
                    break
            self.assist[name] = None

            # Сохраняем изображение
            canvas_img.save(f'{self.destination}/{cover_name}.jpg', quality=quality, dpi=(300, 300))
            canvas_img.close()
        
            AppManager.pf.filebar.step_end()
