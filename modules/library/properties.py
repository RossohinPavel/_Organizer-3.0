def full_name(obj_name):
    """Наделяет Объект атрибутом full_name"""
    return ''


def segment(obj_name):
    """Возвращает кортеж значений сегмента для соответствующей категории"""
    seg = ()
    if obj_name in ('Photobook', 'Layflat', 'Album', 'Canvas'):
        seg += ('Премиум',)
    if obj_name in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Subproduct'):
        seg += ('Тираж',)
    return seg


def short_name(obj_name):
    """Возвращает кортеж значений псевдонимов продуктов для соответствующей категории"""
    names = {'Photobook': ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС'), 'Layflat': ('ППК', 'ПК'), 'Album': ('ФБ', 'ПА', 'ПУР'),
             'Journal': ('Журнал',), 'Photofolder': ('Дуо', 'Дуо гор', 'Трио'), 'Canvas': ('+холсты',),
             'Subproduct': ('+полигр фото', '+открытки', '+магниты')}
    return names[obj_name]


def product_format(obj_name):
    """Возвращает кортеж значений возможных форматов продуктов для соответствующей категории"""
    bf = ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г', '30x40в')
    canvas = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
              '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз')
    formats = {'Photobook': bf[:-1], 'Layflat': bf[4:9], 'Album': bf[4:], 'Journal': bf[4:6], 'Photofolder': bf[5:7],
               'Canvas': canvas}
    return formats[obj_name]


def book_option(obj_name):
    """Возвращает кортеж значений опций сборки продуктов для соответствующей категории"""
    return ('б/у', 'с/у', 'с/у1.2')


def lamination(obj_name):
    """Возвращает кортеж значений типов ламинации для соответствующей категории"""
    return ('гля', 'мат')


def cover_type(obj_name):
    """Возвращает кортеж значений типов обложки для соответствующей категории"""
    ct = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
    return {'Photobook': ct, 'Layflat': ct[:2], 'Album': ct[:1]}[obj_name]


def carton_length(obj_name):
    """Установка значения длинны картона"""
    return 0


def carton_height(obj_name):
    """Установка значения высоты картона"""
    return 0


def cover_clapan(obj_name):
    """Возращает коретеж занчений клапана обложки"""
    return (15, 20)


def cover_joint(obj_name):
    """Возвращает кортеж значений шарнира обложки"""
    return (10, 15, 18)


def print_mat(pos):
    """Общая ф-я печатного материала"""
    cvr_photo = ('Fuji CA Matte 203x406', 'Fuji CA Matte 203x500', 'Fuji CA Matte 254x400', 'Fuji CA Matte 254x500',
                 'Fuji CA Matte 254x700', 'Fuji CA Matte 254x470', 'Fuji CA Matte 305x600', 'Fuji CA Matte 203x570',
                 'Fuji CA Matte 254x620', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x675')
    cvr_poly = ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700')
    pg_photo = ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305', 'Fuji CA Matte 203x400',
                'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512', 'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402',
                'Fuji CA Matte 305x610', 'Fuji CA Matte 305x810')
    pg_poly = ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 170', 'UPM SRA4 150', 'UPM SRA4 250', 'UPM SRA3 170',
               'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
    dct = {'cover': {'Photobook': cvr_photo + cvr_poly, 'Layflat': cvr_poly, 'Album': cvr_poly, 'Journal': pg_poly,
                     'Photofolder': cvr_poly[2:], 'Canvas': ('CottonCanvas',), 'Subproduct': pg_poly},
           'page': {'Photobook': pg_photo, 'Layflat': pg_poly[:-2], 'Album': pg_poly, 'Journal': pg_poly[:-2]}
           }
    return dct[pos]


def cover_print_mat(obj_name):
    """Возвращает кортеж значений печатного материала обложек"""
    return print_mat('cover')[obj_name]


def page_print_mat(obj_name):
    """Возвращает кортеж значений печатного материала разворотов"""
    return print_mat('page')[obj_name]


def cover_canal(obj_name):
    """Возварщает кортеж значений каналов печати обложки"""
    return ('160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242', '243', '245', '266',
            '36', 'POLI')


def page_canal(obj_name):
    """Возвращает кортеж занчений каналов печати разворотов"""
    return ('201', '214', '203', '204', '205', '207', '275', '274', '276', '271')


def dc_break(obj_name):
    """Установка значения разрыва при раскодировке"""
    return 0


def dc_overlap(obj_name):
    """Установка значения нахлеста при раскодировке"""
    return 0


def dc_top_indent(obj_name):
    """Установка значения отступа сверху при раскодировке"""
    return 0


def dc_left_indent(obj_name):
    """Установка значения отступа слева при раскодировке"""
    return 0
