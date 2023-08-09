import random


def dec1(func):
    def wrapper(param):
        print('Вызов декоратора 1: я проверяю кеш')
        return func(param)
    return wrapper


def dec2(func):
    def wrapper(param):
        print('Вызов декоратора 2Ж я подключаюсь к базе данных')
        return func(param)
    return wrapper


@dec1
@dec2
def test_func(some_param):
    return some_param


print(test_func(4))