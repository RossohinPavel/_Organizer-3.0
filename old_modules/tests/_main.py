def print_func_call(func):
    def wrapper(*args, **kwargs):
        print(f'Вызов функции {func.__name__}')
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    wrapper.__doc__ = func.__doc__
    return wrapper


def print_method_call(cls):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)):
            setattr(cls, attr, print_func_call(getattr(cls, attr)))
    return cls
