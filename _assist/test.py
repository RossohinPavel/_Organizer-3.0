def test_decorator(func):
    def wrapper(*args, **kwargs):
        attr = 'test'
        return func(*args, **kwargs)

    return wrapper


@test_decorator
def test():
    print(attr)


test()
