class Product:
    """Конструктор продуктов"""
    _categories = ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas', 'Subproduct')  # Не изменять!
    _rusnames = ('Фотокниги на Фотобумаге', 'Полиграфические фотокниги Layflat',
                 'Полиграфические альбомы, PUR, FlexBind', 'Полиграфические фотожурналы', 'Фотопапки', 'Фотохолсты',
                 'Остальное')
    __segments = ('Премиум', 'Тираж')
    __short_names = ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС', 'ППК', 'ПК', 'ФБ', 'ПА', 'ПУР', 'Журнал', 'Дуо', 'Дуо гор',
                     'Трио', '+холсты', '+полигр фото', '+открытки')
    __book_formats = ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г',
                      '30x40в')
    __canvas_formats = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50',
                        '50x75 верт', '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт',
                        '80x120 гориз')
    __book_options = ('б/у', 'с/у', 'с/у1.2')
    __laminations = ('гля', 'мат')
    __cover_types = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
    __cover_clapan_values = (15, 20)
    __cover_joint_values = (10, 15, 18)
    __cover_photo_mat = ('Fuji CA Matte 152x204', 'Fuji CA Matte 152x304', 'Fuji CA Matte 152x370',
                         'Fuji CA Matte 203x305', 'Fuji CA Matte 203x406', 'Fuji CA Matte 203x470',
                         'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                         'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620',
                         'Fuji CA Matte 254x700', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x610',
                         'Fuji CA Matte 305x675')
    __cover_poly_mat = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
    __page_photo_mat = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305',
                        'Fuji CA Matte 203x400', 'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512',
                        'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402', 'Fuji CA Matte 305x610',
                        'Fuji CA Matte 305x810')
    __page_poly_mat = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 170', 'UPM SRA4 150', 'UPM SRA4 250', 'UPM SRA3 170',
                       'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
    __cover_canal = ('160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242', '243', '245',
                     '266', '36', 'ORAJET', 'POLI')
    __page_canal = ('201', '214', '203', '204', '205', '207', '275', '274', '276', '271')

    @classmethod
    def __get_slice(cls, constant, start=0, end=None):
        """Вспомогательная ф-я для получения срезов из постоянных элементов"""
        return constant[start:end]

    @classmethod
    def translator(cls, name: str, always_eng=False) -> str:
        """Используется для перевода русского названия продукта в английское и обратно"""
        string = ''
        if name in cls._rusnames:
            string = cls._categories[cls._rusnames.index(name)]
        if name in cls._categories:
            string = name if always_eng else cls._rusnames[cls._categories.index(name)]
        return string

    def __new__(cls, product_name: str = 'Subproduct'):
        obj = super().__new__(cls)
        obj._category = cls.translator(product_name, always_eng=True)
        return obj

    def __str__(self):
        return self._category

    def __init__(self, *args, **kwargs):
        self.full_name = ''  # Обязательный и одинаковый для всех продуктов атрибут
        func_dct = {'segment': self.__get_segment,
                    'short_name': self.__get_short_name,
                    'product_format': self.__get_product_format,
                    'book_option': lambda: self.__book_options,
                    'lamination': lambda: self.__laminations,
                    'cover_type': self.__cover_type,
                    'carton_length': lambda: 0,
                    'carton_height': lambda: 0,
                    'cover_clapan': lambda: self.__cover_clapan_values,
                    'cover_joint': lambda: self.__cover_joint_values,
                    'cover_print_mat': self.__get_cover_print_mat,
                    'page_print_mat': self.__get_page_print_mat,
                    'cover_canal': lambda: self.__cover_canal, 'page_canal': lambda: self.__page_canal,
                    'dc_break': lambda: 0, 'dc_overlap': lambda: 0,
                    'dc_top_indent': lambda: 0, 'dc_left_indent': lambda: 0}
        for attr in self.__get_attr_list():
            if attr in func_dct:
                setattr(self, attr, func_dct[attr]())  # Наделяем объект соответствующими атрибутами

    def __get_attr_list(self) -> tuple:
        """Функция для получения списка атрибутов, которые соответствуют категории продукта
        :return: Кортеж из функций, которые в свою очередь возвращают (имя атрибута, соответствующие категории значения)
        """
        attr_list = {'Photobook': ('segment', 'short_name', 'product_format', 'book_option', 'lamination', 'cover_type',
                                   'carton_length', 'carton_height', 'cover_clapan', 'cover_joint', 'cover_print_mat',
                                   'page_print_mat', 'cover_canal', 'page_canal'),
                     'Layflat': ('segment', 'short_name', 'product_format', 'book_option', 'lamination', 'cover_type',
                                 'carton_length', 'carton_height', 'cover_clapan', 'cover_joint', 'cover_print_mat',
                                 'page_print_mat'),
                     'Album': ('segment', 'short_name', 'product_format', 'lamination', 'cover_type', 'carton_length',
                               'carton_height', 'cover_clapan', 'cover_joint', 'cover_print_mat', 'page_print_mat',
                               'dc_break', 'dc_overlap', 'dc_top_indent', 'dc_left_indent'),
                     'Journal': ('segment', 'short_name', 'product_format', 'cover_print_mat', 'page_print_mat'),
                     'Photofolder': ('segment', 'short_name', 'product_format', 'lamination', 'carton_length',
                                     'carton_height', 'cover_clapan', 'cover_joint', 'cover_print_mat'),
                     'Canvas': ('segment', 'short_name', 'product_format', 'cover_print_mat'),
                     'Subproduct': ('segment', 'short_name', 'cover_print_mat')}
        return attr_list[self._category]

    def __get_segment(self):
        """Возвращает имя атрибута (segment) и соответствующие категории значения segment"""
        if self._category == 'Canvas':
            return self.__segments[:1]
        if self._category in ('Journal', 'Photofolder', 'Subproduct'):
            return self.__segments[1:]
        return self.__segments

    def __get_short_name(self):
        """Возвращает имя атрибута (short_name) и соответствующие категории значения short_name"""
        short_n = {'Photobook': (0, 5), 'Layflat': (5, 7), 'Album': (7, 10), 'Journal': (10, 11),
                   'Photofolder': (11, 14), 'Canvas': (14, 15), 'Subproduct': (15, 17)}
        return self.__get_slice(self.__short_names, *short_n[self._category])

    def __get_product_format(self):
        """Возвращает имя атрибута (product_format) и соответствующие категории значения book_format"""
        if self._category == 'Canvas':
            return self.__canvas_formats
        pf = {'Photobook': (), 'Layflat': (4, 9), 'Album': (4, ), 'Journal': (4, 6), 'Photofolder': (5, 7)}
        return self.__get_slice(self.__book_formats, *pf[self._category])

    def __cover_type(self):
        """Возвращает имя атрибута (cover_type) и соответствующие категории значения cover_type"""
        res = {'Photobook': (), 'Layflat': (0, 2), 'Album': (0, 1)}[self._category]
        return self.__get_slice(self.__cover_types, *res)

    def __get_cover_print_mat(self):
        pm = {'Photobook': lambda: self.__cover_photo_mat + self.__cover_poly_mat,
              'Layflat': lambda: self.__cover_poly_mat,
              'Album': lambda: self.__cover_poly_mat,
              'Journal': lambda: self.__page_poly_mat,
              'Photofolder': lambda: self.__cover_poly_mat[:2],
              'Canvas': lambda: ('CottonCanvas',),
              'Subproduct': lambda: self.__page_poly_mat}
        return pm[self._category]()

    def __get_page_print_mat(self):
        if self._category == 'Photobook':
            return self.__page_photo_mat
        return self.__page_poly_mat


if __name__ == '__main__':
    import modules.tests as tst

    tst.product_test(Product)
