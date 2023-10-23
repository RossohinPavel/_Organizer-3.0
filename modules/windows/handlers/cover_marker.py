from .handler import HandlerWindow
from ...file_handlers import CoverMarkerHandler


class CoverMarker(HandlerWindow):
    """Разметка обложки"""
    win_title = 'Разметка обложек'
    handler_description = 'Разметка обратной стороны для обложкек.\nВ заказе будут обработаны все определившиеся ' \
                          'тиражи\nсогласно спецификации продукта. Для индивидуальных\nобложек файлы с сетками ' \
                          'будут сохранены в папке\nCovers, для одинаковых - Constant. При выборе опции\nобработки ' \
                          '\'Добавление бэкпринта\' на заднюю часть\nобложки будет нанесена информация о названии\n' \
                          'тиража и особенностях сборки продукта.'
    handler_option_text = 'Добавление бэкпринта'
    file_handler = CoverMarkerHandler()

    def handler_predicate(self, product_obj) -> object | None:
        if product_obj is None:
            return None
        if product_obj.category in ('Album', 'Layflat', 'Photobook') and product_obj.cover_type in ('Книга', 'Планшет'):
            return product_obj
        return None
