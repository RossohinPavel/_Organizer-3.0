from ._handler import HandlerWindow
from ...file_handlers import CanvasHandler


class CanvasHandlerWindow(HandlerWindow):
    win_title = 'Обработчик холстов'
    handler_description = 'Подготовка изображений для галерейной натяжки холстов.\n3 сантиметра по периметру '\
                          'изображения будут залиты белым.\nПри выборе опции \'Дополнительная подрезка '\
                          'изображения\'\nразмер изображения будет сокращен на 2 сантиметра с каждой\nстороны '\
                          'при сохранении масштаба. Вместо 3 сантиметров\nна загиб останется 2. '\
                          'Изображения будут сохранены в корневом\nкаталоге заказа и переименованы '\
                          'согласно спецификации продукта.'
    handler_option_text = 'Дополнительная подрезка изображения'
    file_handler = CanvasHandler()

    def handler_predicate(self, product_obj) -> object | None:
        return product_obj if product_obj.category == 'Canvas' else None
