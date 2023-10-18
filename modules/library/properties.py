class Blank:
    """Класс наделяющий объект продукта соответствующими свойствами"""
    __slots__ = 'product_obj'

    def __init__(self, category):
        self.product_obj = category()

    def create_blank(self) -> object:
        """Наделяет объект продукта свойствами и возвращает его"""
        category = self.product_obj.__class__.__name__
        for slot in self.product_obj.__slots__:
            eval(f'self._{slot}(category)')
        return self.product_obj

    def _full_name(self, category: str):
        self.product_obj.full_name = ''

    def _segment(self, category: str):
        """Наделяет продукт кортежем значений сегмента для соответствующей категории"""
        self.product_obj.segment = ()
        if category in ('Photobook', 'Layflat', 'Album', 'Canvas'):
            self.product_obj.segment += ('Премиум',)
        if category in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Subproduct'):
            self.product_obj.segment += ('Тираж',)

    def _short_name(self, category: str):
        """Наделяет продукт кортежем значений псевдонимов для соответствующей категории"""
        names = {'Photobook': ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС'),
                 'Layflat': ('ППК', 'ПК'),
                 'Album': ('ФБ', 'ПА', 'ПУР'),
                 'Journal': ('Журнал',),
                 'Photofolder': ('Дуо', 'Дуо гор', 'Трио'),
                 'Canvas': ('+холсты',),
                 'Subproduct': ('+полигр фото', '+открытки', '+магниты')}
        self.product_obj.short_name = names[category]

    def _product_format(self, category: str):
        """Наделяет продукт кортежем значений возможных форматов продуктов для соответствующей категории"""
        bf = ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г', '30x40в')
        canvas = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
                  '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз')
        formats = {'Photobook': bf[:-1],
                   'Layflat': bf[4:9],
                   'Album': bf[4:],
                   'Journal': bf[4:6],
                   'Photofolder': bf[5:7],
                   'Canvas': canvas}
        self.product_obj.product_format = formats[category]

    def _book_option(self, category: str):
        """Наделяет продукт кортежем значений опций сборки продуктов для соответствующей категории"""
        self.product_obj.book_option = ('б/у', 'с/у', 'с/у1.2')

    def _lamination(self, category: str):
        """Наделяет продукт кортежем значений типов ламинации для соответствующей категории"""
        self.product_obj.lamination = ('гля', 'мат')

    def _cover_type(self, category: str):
        """Наделяет продукт кортежем значений типов обложки для соответствующей категории"""
        ct = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
        self.product_obj.cover_type = {'Photobook': ct, 'Layflat': ct[:2], 'Album': ct[:1]}[category]

    def _carton_length(self, category: str):
        """Установка значения длинны картона"""
        self.product_obj.carton_length = 0

    def _carton_height(self, category: str):
        """Установка значения высоты картона"""
        self.product_obj.carton_height = 0

    def _cover_clapan(self, category: str):
        """Наделяет продукт кортежем значений клапана обложки"""
        self.product_obj.cover_clapan = (15, 20)

    def _cover_joint(self, category: str):
        """Наделяет продукт кортежем значений шарнира обложки"""
        self.product_obj.cover_joint = (10, 15, 18)

    @staticmethod
    def __print_mat(pos):
        """Общая ф-я печатного материала"""
        cvr_photo = ('Fuji CA Matte 203x406', 'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                     'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620', 'Fuji CA Matte 254x700',
                     'Fuji CA Matte 254x770', 'Fuji CA Matte 305x600', 'Fuji CA Matte 305x675')
        cvr_poly = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
        pg_photo = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305', 'Fuji CA Matte 203x400',
                    'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512', 'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402',
                    'Fuji CA Matte 305x610', 'Fuji CA Matte 305x810')
        pg_poly = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 150', 'UPM SRA4 170', 'UPM SRA4 250', 'UPM SRA3 170',
                   'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
        dct = {'cover': {'Photobook': cvr_photo + cvr_poly,
                         'Layflat': cvr_poly,
                         'Album': cvr_poly,
                         'Journal': pg_poly,
                         'Photofolder': cvr_poly[2:],
                         'Canvas': ('CottonCanvas',),
                         'Subproduct': pg_poly + ('MagnetycVinyl', )},
               'page': {'Photobook': pg_photo,
                        'Layflat': pg_poly[:-2],
                        'Album': pg_poly,
                        'Journal': pg_poly[:-2]}
               }
        return dct[pos]

    def _cover_print_mat(self, category: str):
        """Наделяет продукт кортежем значений печатного материала обложек"""
        self.product_obj.cover_print_mat = self.__print_mat('cover')[category]

    def _page_print_mat(self, category: str):
        """Наделяет продукт кортежем значений печатного материала разворотов"""
        self.product_obj.page_print_mat = self.__print_mat('page')[category]

    def _cover_canal(self, category: str):
        """Наделяет продукт кортежем значений каналов печати обложки"""
        self.product_obj.cover_canal = ('36', '160', '161', '162', '163', '164', '165', '166', '204', '205', '214',
                                        '240', '242', '243', '245', '266', 'POLI')

    def _page_canal(self, category: str):
        """Наделяет продукт кортежем занчений каналов печати разворотов"""
        self.product_obj.page_canal = ('201', '203', '204', '205', '207', '214', '271', '274', '275', '276')

    def _dc_break(self, category: str):
        """Установка значения разрыва при раскодировке"""
        self.product_obj.dc_break = 0

    def _dc_overlap(self, category: str):
        """Установка значения нахлеста при раскодировке"""
        self.product_obj.dc_overlap = 0

    def _dc_top_indent(self, category: str):
        """Установка значения отступа сверху при раскодировке"""
        self.product_obj.dc_top_indent = 0

    def _dc_left_indent(self, category: str):
        """Установка значения отступа слева при раскодировке"""
        self.product_obj.dc_left_indent = 0
