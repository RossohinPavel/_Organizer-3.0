class Test:
    attr = None

    def __new__(cls):
        cls.attr = cls.__name__
        return super().__new__(cls)


class Test1(Test):

    def __new__(cls):
        res = super().__new__(cls)
        super(cls, res).__setattr__('test', 1)
        return res
    
    def __setattr__(self, __name: str, __value) -> None:
        print('__setattr__', self.__class__.__name__)
        super().__setattr__(__name, __value)

class Test2(Test): pass


t = Test()
t1 = Test1()
t2 = Test2()
