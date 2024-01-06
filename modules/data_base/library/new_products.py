from typing import NamedTuple


class Product(NamedTuple):
    """Представление атрибутов продукта."""

    # Обязательные атрибуты для каждого продукта.
    name: str               # Название продукта
    type: str               # Тип продукта, Альбом, Пур, Журнал и т.д
    segment: str            # Сегмент продукции, премиум или тираж
    short_name: str         # Короткое имя, используемое в наклейке
    format: str             # Формат книги

    # Необязательные атрибуты. Содеражат значение, если для 
    # продукта определен этот атрибут. None в противном случае.

    # Атрибуты обложки
    cover_type: str
    carton_length: int
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str
    cover_lam: str

    # Атрибуты внутреннего блока
    page_option: str
    page_print_mat: str
    page_lam: str

    # Атрибуты для раскодировки      
    dc_top_indent: int
    dc_left_indent: int
    dc_overlap: int
    dc_break: int
