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