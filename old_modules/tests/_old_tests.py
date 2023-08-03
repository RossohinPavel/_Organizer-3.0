import time
import threading
from old_modules.library import Library


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
    obj_lst = [product_class.blank(x) for x in product_class.get_categories()]
    for ind, obj in enumerate(obj_lst):
        # Общие тесты
        assert 'full_name' in obj, f'Отсутствует строка для указания полного имени в {str(obj)}'
        print(obj['full_name'], '- ', end='')
        assert obj['segment'] != (), f'Отсутствует указание сегмента продукции в {str(obj)}'
        assert obj['short_name'] != (), f'Отсутствует список коротких имен в {str(obj)}'
        # Формат книг
        if ind in range(6):
            assert obj['product_format'] != (), f'Отсутствует указание формата продукта в {str(obj)}'
        # Утолщение
        if ind in (0, 1):
            assert obj['book_option'] != (), f'Отсутствует указание утолщения продукта в {str(obj)}'
        # # Ламинация
        if ind in (0, 1, 2, 4):
            assert obj['lamination'] != (), f'Отсутствует указание ламинации в {str(obj)}'
        # # Тип оболожки
        if ind in range(3):
            assert obj['cover_type'] != (), f'Отсутствует указание списка типов обложки в {str(obj)}'
        # # Размер Картонки
        if ind in (0, 1, 2, 4):
            assert obj['carton_length'] == 0, f'Отсутствует указание длинны картона в {str(obj)}'
            assert obj['carton_height'] == 0, f'Отсутствует указание высоты картона в {str(obj)}'
        # клапан и шарнир
        if ind in (0, 1, 2):
            assert obj['cover_clapan'] != (), f'Отсутствует указание значений клапана в {str(obj)}'
            assert obj['cover_joint'] != (), f'Отсутствует указание значений шарнира в {str(obj)}'
        # Печатный материал обложек
        assert obj['cover_print_mat'] != (), f'Отсутствует cписок печатного материала обложек в {str(obj)}'
        # Печатный материал разворотов
        if ind in range(4):
            assert obj['page_print_mat'] != (), f'Отсутствует печатного материала разворота в {str(obj)}'
        # """Частные тесты продуктов"""
        if str(obj) == 'Photobook':
            assert 'cover_canal' in obj.__dict__
            assert 'page_canal' in obj.__dict__
        if str(obj) == 'Album':
            assert 'dc_break' in obj.__dict__
            assert 'dc_overlap' in obj.__dict__
            assert 'dc_top_indent' in obj.__dict__
            assert 'dc_left_indent' in obj.__dict__
        print()


def library_multithread_test(lib_obj):
    def test_read_lib(lib_obj):
        func = lib_obj.get_product_values
        param = ('Photobook', 'Photobook_test')
        print(func(*param))
        print(lib_obj._cache_clear)
        print(func(*param))

    def test_read_lib1(lib_obj):
        func = lib_obj.get_product_values
        param = ('Photobook', 'Photobook_test')
        print(func(*param))
        print(func(*param))

    th1 = threading.Thread(target=test_read_lib, args=(lib_obj, ))
    th2 = threading.Thread(target=test_read_lib1, args=(lib_obj, ))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


if __name__ == '__main__':
    lib = Library()
    library_multithread_test(lib)