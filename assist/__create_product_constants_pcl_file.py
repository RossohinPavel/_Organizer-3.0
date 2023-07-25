"""Создает или заменяет файл product_constants.pcl"""
import pickle


CONSTANTS = {'SEGMENT': ('Премиум', 'Тираж'),
             'SHORT_NAMES': ('КС', 'ЛЮКС', 'кКожа', 'КК', 'ПС', 'ППК', 'ПК', 'ПА', 'ПУР', 'ФБ', 'Журнал', 'Дуо',
                             'Дуо гор', 'Трио', '+холсты', '+полигр фото', '+открытки'),
             'PRODUCT_FORMATS': ('10x10', '15x15', '15x20в', '20x15г', '20x20', '20x30в', '30x20г', '25x25', '30x30',
                                 '40x30г', '30x40в'),
             'CANVAS_FORMATS': ('30x45 верт', '30x45 гориз', '40x40', '40x60 верт', '40x60 гориз', '45x45', '50x50',
                                '50x75 верт', '50x75 гориз', '60x60', '60x90 верт', '60x90 гориз', '80x80',
                                '80x120 верт', '80x120 гориз'),
             'BOOK_OPTIONS': ('б/у', 'с/у', 'с/у1.2'),
             'LAMINATION': ('гля', 'мат'),
             'COVER_TYPES': ('Книга', 'Планшет', 'ЛЮКС', 'Кожаный корешок', 'Кожаная обложка'),
             'PHOTO_COVER_MATERIAL': ('Fuji CA Matte 152x204', 'Fuji CA Matte 152x304', 'Fuji CA Matte 152x370',
                                      'Fuji CA Matte 203x305', 'Fuji CA Matte 203x406', 'Fuji CA Matte 203x470',
                                      'Fuji CA Matte 203x500', 'Fuji CA Matte 203x570', 'Fuji CA Matte 254x400',
                                      'Fuji CA Matte 254x470', 'Fuji CA Matte 254x500', 'Fuji CA Matte 254x620',
                                      'Fuji CA Matte 254x700', 'Fuji CA Matte 254x770', 'Fuji CA Matte 305x610',
                                      'Fuji CA Matte 305x675'),
             'PHOTO_PAGE_MATERIAL': ('Fuji CA Matte 152x304', 'Fuji CA Matte 152x406', 'Fuji CA Matte 203x305',
                                     'Fuji CA Matte 203x400', 'Fuji CA Matte 203x600', 'Fuji CA Matte 254x512',
                                     'Fuji CA Matte 300x102', 'Fuji CA Matte 305x402', 'Fuji CA Matte 305x610',
                                     'Fuji CA Matte 305x810'),
             'COVER_CANAL': ('POLI', '160', '161', '162', '163', '164', '165', '166', '204', '205', '214', '240', '242',
                             '243', '245', '266', '36'),
             'PAGE_CANAL': ('201', '214', '203', '204', '205', '207', '275', '274', '276', '271'),
             'POLY_COVER_MATERIAL': ('Omela 500', 'Omela 700', 'Raflatac 500', 'Raflatac 700'),
             'POLY_PAGE_MATERIAL': ('Sappi SRA3', 'Sappi 320x620', 'UPM SRA4 170', 'UPM SRA4 150', 'UPM SRA4 250',
                                    'UPM SRA3 170', 'UPM SRA3 250', 'Flex Bind 330x330', 'Flex Bind 320x450')
             }


if __name__ == '__main__':
    print('Вы точно хотите обновить product_constants.pcl? Y/N')
    if input() == 'Y':
        with open('../modules/library/product_constants.pcl', 'wb') as file:
            pickle.dump(CONSTANTS, file)
    with open('../modules/library/product_constants.pcl', 'rb') as file:
        print(pickle.load(file))