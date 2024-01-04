from ._handler import *
# from ...file_handlers import CanvasHandler


class CanvasHandlerWindow(HandlerWindow):
    win_title = 'Обработчик холстов'
    handler_description = """
        Подготовка изображений для галерейной натяжки холстов. 3 сантиметра по периметру
        изображения будут залиты белым. При выборе опции \'Дополнительная подрезка изображения\'
        размер изображения будет сокращен (по 1 сантиметру с каждой стороны) при сохранении 
        масштаба. Вместо 3 сантиметров на загиб останется 2. Изображения будут сохранены в 
        корневом каталоге заказа и переименованы согласно спецификации продукта.
    """
    handler_option_text = 'Дополнительная подрезка изображения'
    # file_handler = CanvasHandler()

    def handler_predicate(self, product_obj: Categories) -> Categories | None:
        return product_obj if product_obj.category == 'Canvas' else None
