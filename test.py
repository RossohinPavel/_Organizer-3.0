import random


def test_decorator(check=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            res = func(*args, **kwargs)
            if check:
                res *= 2
            return res
        return wrapper
    return decorator


@test_decorator(True)
def test_func(some_param):
    return some_param


print(test_func(4))