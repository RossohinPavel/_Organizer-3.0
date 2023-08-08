def product_test(product_class):
    """Тестирование конструктора продуктов на полноту генерируемых категорий"""
    obj_lst = [product_class(x, True) for x in product_class.get_categories()]
    for obj in obj_lst:     # Проверяем на присутсвие атрибутов
        name = obj.__class__.__name__
        print(obj)
        # Общие тесты
        assert 'full_name' in obj, f'Отсутствует строка для указания полного имени в {name}'
        assert obj['full_name'] == '', f'Отсутствует значение по умолчанию для full_name в {name}'
        assert 'segment' in obj, f'Отсутствует указание сегмента продукции в {name}'
        assert obj['segment'] != (), f'Отсутствует значение по умолчанию для segment в {name}'
        assert 'short_name' in obj, f'Отсутствует список коротких имен в {name}'
        assert obj['short_name'] != (), f'Отсутствует значение по умолчанию для short_name в {name}'
        # Формат книг
        if name in ('Photobook', 'Layflat', 'Album', 'Journal', 'Photofolder', 'Canvas'):
            assert 'product_format' in obj, f'Отсутствует указание формата продукта в {name}'
            assert obj['product_format'] != (), f'Отсутствует значение по умолчанию для product_format в {name}'
        # Утолщение
        if name in ('Photobook', 'Layflat'):
            assert 'book_option' in obj, f'Отсутствует указание утолщения продукта в {name}'
            assert obj['book_option'] != (), f'Отсутствует значение по умолчанию для book_option в {name}'
        # Ламинация
        if name in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            assert 'lamination' in obj, f'Отсутствует указание ламинации в {name}'
            assert obj['lamination'] != (), f'Отсутствует значение по умолчанию для lamination в {name}'
        # Тип оболожки
        if name in ('Photobook', 'Layflat', 'Album'):
            assert 'cover_type' in obj, f'Отсутствует указание списка типов обложки в {name}'
            assert obj['cover_type'] != (), f'Отсутствует значение по умолчанию для cover_type в {name}'
        # Размер Картонки
        if name in ('Photobook', 'Layflat', 'Album', 'Photofolder'):
            assert 'carton_length' in obj, f'Отсутствует указание длинны картона в {name}'
            assert obj['carton_length'] == 0, f'Отсутствует значение по умолчанию для carton_length в {name}'
            assert 'carton_height' in obj, f'Отсутствует указание высоты картона в {name}'
            assert obj['carton_height'] == 0, f'Отсутствует значение по умолчанию для carton_height в {name}'
        # Клапан и шарнир
        if name in ('Photobook', 'Layflat', 'Album'):
            assert 'cover_clapan' in obj, f'Отсутствует указание значений клапана в {name}'
            assert obj['cover_clapan'] != (), f'Отсутствует значение по умолчанию для cover_clapan в {name}'
            assert 'cover_joint' in obj, f'Отсутствует указание значений шарнира в {name}'
            assert obj['cover_joint'] != (), f'Отсутствует значение по умолчанию для cover_joint в {name}'
        # Печатный материал обложек
        assert 'cover_print_mat' in obj, f'Отсутствует cписок печатного материала обложек в {name}'
        assert obj['cover_print_mat'] != (), f'Отсутствует значение по умолчанию для cover_print_mat в {name}'
        # Печатный материал разворотов
        if name in ('Photobook', 'Layflat', 'Album', 'Journal'):
            assert 'page_print_mat' in obj, f'Отсутствует печатного материала разворота в {obj}'
            assert obj['page_print_mat'] != (), f'Отсутствует значение по умолчанию для page_print_mat в {name}'
        # """Частные тесты продуктов"""
        if name == 'Photobook':
            assert 'cover_canal' in obj
            assert obj['cover_canal'] != (), f'Отсутствует значение по умолчанию для cover_canal в {name}'
            assert 'page_canal' in obj
            assert obj['page_canal'] != (), f'Отсутствует значение по умолчанию для page_canal в {name}'
        if name == 'Album':
            assert 'dc_break' in obj
            assert obj['dc_break'] == 0, f'Отсутствует значение по умолчанию для dc_break в {name}'
            assert 'dc_overlap' in obj
            assert obj['dc_overlap'] == 0, f'Отсутствует значение по умолчанию для dc_overlap в {name}'
            assert 'dc_top_indent' in obj
            assert obj['dc_top_indent'] == 0, f'Отсутствует значение по умолчанию для dc_top_indent в {name}'
            assert 'dc_left_indent' in obj
            assert obj['dc_left_indent'] == 0, f'Отсутствует значение по умолчанию для dc_left_indent в {name}'
