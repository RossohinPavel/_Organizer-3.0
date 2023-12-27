from typing import NamedTuple
from pympler.asizeof import asizeof


class Methods:
    __slots__ = ()

    @property
    def category(self): 
        return self.__class__.__name__


class Album(NamedTuple):
    """Полиграфически Альбомы, Pur, FlexBind"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта  
    short_name: str
    product_format: str
    lamination: str
    cover_type: str               # Тип сборки обложки
    carton_length: int            # Технические размеры обложки
    carton_height: int
    cover_flap: int
    cover_joint: int
    cover_print_mat: str          # Печатный материал
    page_print_mat: str           
    dc_top_indent: int            # Индивидуальные особенности продукта
    dc_left_indent: int
    dc_overlap: int
    dc_break: int


class NewAlbum(Album, Methods):
    __slots__ = ()
    pass


print(asizeof(Album('1', '1', '1', '1', '1', '1', 1, 1, 1, 1, '1', '1', 1, 1, 1, 1)))

print(asizeof(NewAlbum('1', '1', '1', '1', '1', '1', 1, 1, 1, 1, '1', '1', 1, 1, 1, 1)))