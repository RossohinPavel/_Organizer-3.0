import time


def func_time_test(cycles=100):
    """тестирование ф-ии на время выполнения"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            for _ in range(cycles):
                func(*args, **kwargs)
            res = func(*args, **kwargs)
            print(f'Время {cycles} циклов функции {wrapper.__name__} -', time.time() - start)
            return res
        return wrapper
    return decorator


def product_test(product_class):
    """Тестирование конструктора продуктов на полноту генерируемых категорий"""
    obj_lst = [product_class(x) for x in product_class._categories]
    for obj in obj_lst:
        # Общие тесты
        assert obj._category != '', f'Отсутствует указание категории продукции в {str(obj)}'
        assert 'full_name' in obj.__dict__, f'Отсутствует строка для указания полного имени в {str(obj)}'
        assert obj.__dict__['segment'] != (), f'Отсутствует указание сегмента продукции в {str(obj)}'
        assert obj.__dict__['short_name'] != (), f'Отсутствует список коротких имен в {str(obj)}'
        # Формат книг
        if str(obj) in ('Photofolder', 'Canvas', 'Journal', 'Album', 'Layflat', 'Photobook'):
            assert 'product_format' in obj.__dict__ and obj.__dict__['product_format'] != (), f'Отсутствует указание формата продукта в {str(obj)}'
        # Утолщение
        if str(obj) in ('Layflat', 'Photobook'):
            assert 'book_option' in obj.__dict__ and obj.__dict__['book_option'] != (), f'Отсутствует указание утолщения продукта в {str(obj)}'
        # Ламинация
        if str(obj) in ('Photofolder', 'Album', 'Layflat', 'Photobook'):
            assert 'lamination' in obj.__dict__ and obj.__dict__['lamination'] != (), f'Отсутствует указание ламинации в {str(obj)}'
        # # Тип оболожки
        if str(obj) in ('Album', 'Layflat', 'Photobook'):
            assert 'cover_type' in obj.__dict__ and obj.__dict__['cover_type'] != (), f'Отсутствует указание списка типов обложки в {str(obj)}'
        # Размер Картонки, клапан и шарнир
        if str(obj) in ('Photofolder', 'Album', 'Layflat', 'Photobook'):
            assert 'carton_length' in obj.__dict__ and obj.__dict__['carton_length'] == 0, f'Отсутствует указание длинны картона в {str(obj)}'
            assert 'carton_height' in obj.__dict__ and obj.__dict__['carton_height'] == 0, f'Отсутствует указание высоты картона в {str(obj)}'
            assert 'cover_clapan' in obj.__dict__ and obj.__dict__['cover_clapan'] != (), f'Отсутствует указание значений клапана в {str(obj)}'
            assert 'cover_joint' in obj.__dict__ and obj.__dict__['cover_joint'] != (), f'Отсутствует указание значений шарнира в {str(obj)}'
        # Печатный материал обложек
        assert obj.__dict__['cover_print_mat'] != (), f'Отсутствует cписок печатного материала обложек в {str(obj)}'
        # Печатный материал разворотов
        if str(obj) in ('Journal', 'Album', 'Layflat', 'Photobook'):
            assert 'page_print_mat' in obj.__dict__ and obj.__dict__['page_print_mat'] != (), f'Отсутствует печатного материала разворота в {str(obj)}'
        # """Частные тесты продуктов"""
        if str(obj) == 'Photobook':
            assert 'cover_canal' in obj.__dict__
            assert 'page_canal' in obj.__dict__
        if str(obj) == 'Album':
            assert 'dc_break' in obj.__dict__
            assert 'dc_overlap' in obj.__dict__
            assert 'dc_top_indent' in obj.__dict__
            assert 'dc_left_indent' in obj.__dict__
