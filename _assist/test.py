def print_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(res)
        return res
    return wrapper



class Test: 
    def __init__(self) -> None:
        print(self.__class__.__dict__)
        self.__class__._some_method = print_decorator(self.__class__._some_method)
        print(self.__class__.__dict__)

    def _some_method(self) -> int:
        return 1

class Test1(Test):
    def _some_method(self) -> int:
        return 2


t = Test1()
t._some_method()
