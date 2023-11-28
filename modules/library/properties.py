from typing import Literal


class Properties:
    """Описание свойств продуктов"""
    __slots__ = '__product_type'

    def __init__(self, category: str):
        self.__product_type = category

    def __call__(self, property: str) -> list[str] | tuple[str]:
        return eval(f'self._{property}()')

    def _segment(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений сегмента для соответствующей категории"""
        segment = ()
        if self.__product_type in ('Photobook', 'Layflat', 'Album', 'Canvas'):
           segment += ('Премиум', )
        if self.__product_type in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Subproduct'):
            segment += ('Тираж', )
        return segment

    def _short_name(self) -> tuple[str, ...]:   # type: ignore
        """Наделяет продукт кортежем значений псевдонимов для соответствующей категории"""
        match self.__product_type:
            case 'Photobook': return ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС')
            case 'Layflat': return ('ППК', 'ПК')
            case 'Album': return ('ФБ', 'ПА', 'ПУР')
            case 'Journal': return ('Журнал',)
            case 'Photofolder': return ('Дуо', 'Дуо гор', 'Трио')
            case 'Canvas': return ('+холсты',)
            case 'Subproduct': return ('+полигр фото', '+открытки', '+магниты')

    def _product_format(self) -> tuple[str, ...]:   # type: ignore
        """Наделяет продукт кортежем значений возможных форматов продуктов для соответствующей категории"""
        bf = ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30', '40x30г', '30x40в')
        canvas = ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50', '50x75 верт',
                  '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80', '80x120 верт', '80x120 гориз')
        match self.__product_type:
            case 'Photobook': return bf[:-1]
            case 'Layflat': return bf[4:9]
            case 'Album': return bf[4:]
            case 'Journal': return bf[4:6]
            case 'Photofolder': return bf[5:7]
            case 'Canvas': return canvas

    def _book_option(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений опций сборки продуктов для соответствующей категории"""
        return ('б/у', 'с/у', 'с/у1.2')

    def _lamination(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений типов ламинации для соответствующей категории"""
        return ('гля', 'мат')

    def _cover_type(self) -> tuple[str, ...]:   # type: ignore
        """Наделяет продукт кортежем значений типов обложки для соответствующей категории"""
        ct = ('Книга', 'Планшет', 'Люкс', 'Кожаный корешок', 'Кожаная обложка')
        match self.__product_type:
            case 'Photobook': return ct
            case 'Layflat': return ct[:2]
            case 'Album': return ct[:1]

    def _cover_flap(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений клапана обложки"""
        return ('15', '20')

    def _cover_joint(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений шарнира обложки"""
        return ('9', '10', '15', '18')

    def __print_mat(self, pos: Literal['cover', 'page']) -> tuple[str, ...]: # type: ignore
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
        match self.__product_type:
            case 'Photobook' if pos == 'cover': return cvr_photo + cvr_poly     # Материал для обложек
            case 'Layflat' if pos == 'cover': return cvr_poly
            case 'Album' if pos == 'cover': return cvr_poly
            case 'Journal' if pos == 'cover': return pg_poly
            case 'Photofolder' if pos == 'cover': return cvr_poly[2:]
            case 'Canvas' if pos == 'cover': return ('CottonCanvas',)
            case 'Subproduct' if pos == 'cover': return pg_poly + ('MagnetycVinyl', 'Silk SRA4')
            case 'Photobook' if pos == 'page': return pg_photo                  # Материал для разворотов
            case 'Layflat' if pos == 'page': return pg_poly[:-2]
            case 'Album' if pos == 'page': return  pg_poly
            case 'Journal' if pos == 'page': return pg_poly[:-2]

    def _cover_print_mat(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений печатного материала обложек"""
        return self.__print_mat('cover')

    def _page_print_mat(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений печатного материала разворотов"""
        return self.__print_mat('page')

    def _cover_canal(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем значений каналов печати обложки"""
        return ('36', '160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242', '243', '245', '266', 'POLI')

    def _page_canal(self) -> tuple[str, ...]:
        """Наделяет продукт кортежем занчений каналов печати разворотов"""
        return ('201', '203', '204', '205', '207', '214', '271', '274', '275', '276')
