class Product:
    """Абстракнтый класс - основание для наследования продуктов. Содержит обязательные свойства для продуктов."""
    rus_name = 'Продукт'
    __slots__ = tuple()     # Слоты так же служат для описания списка свойств того или иного продукта

    def __repr__(self):
        return f'{self.__class__.__name__} <full_name={self.full_name}>'

    @property
    def category(self):
        return self.__class__.__name__

    # def to_dict(self) -> dict:
    #     """Возвращает словарь на основе продукта"""
    #     return {s: getattr(self, s) for s in self.__slots__}

    def __contains__(self, item):
        return item in self.__slots__


class Album(Product):
    rus_name = 'Полиграфические альбомы, PUR, FlexBind'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format', 'lamination',                  # Общие особенности продукта
                 'cover_type',                                                             # Тип сборки обложки
                 'carton_length', 'carton_height', 'cover_clapan', 'cover_joint',          # Технические размеры обложки
                 'cover_print_mat', 'page_print_mat',                                      # Печатный материал
                 'dc_top_indent', 'dc_left_indent', 'dc_overlap', 'dc_break')              # Индивидуальные особенности


class Canvas(Product):
    rus_name = 'Фотохолсты'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format',                                # Общие особенности продукта
                 'cover_print_mat')                                                        # Печатный материал


class Journal(Product):
    rus_name = 'Полиграфические фотожурналы'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format',                                # Общие особенности продукта
                 'cover_print_mat', 'page_print_mat')                                      # Печатный материал


class Layflat(Product):
    rus_name = 'Полиграфические фотокниги Layflat'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format', 'book_option', 'lamination',   # Общие особенности продукта
                 'cover_type',                                                             # Тип сборки обложки
                 'carton_length', 'carton_height', 'cover_clapan', 'cover_joint',          # Технические размеры обложки
                 'cover_print_mat', 'page_print_mat')                                      # Печатный материал


class Photobook(Product):
    rus_name = 'Фотокниги на Фотобумаге'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format', 'book_option', 'lamination',   # Общие особенности продукта
                 'cover_type',                                                             # Тип сборки обложки
                 'carton_length', 'carton_height', 'cover_clapan', 'cover_joint',          # Технические размеры обложки
                 'cover_print_mat', 'page_print_mat',                                      # Печатный материал
                 'cover_canal', 'page_canal')                                              # Индивидуальные особенности


class Photofolder(Product):
    rus_name = 'Фотопапки'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name', 'product_format', 'lamination',                  # Общие особенности продукта
                 'carton_length', 'carton_height',                                         # Технические размеры обложки
                 'cover_print_mat')                                                        # Печатный материал


class Subproduct(Product):
    rus_name = 'Остальное'
    __slots__ = ('full_name',                                                              # Полное имя продукта
                 'segment', 'short_name',                                                  # Общие особенности продукта
                 'cover_print_mat')                                                        # Печатный материал
