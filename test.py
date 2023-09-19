class Test:
   
    def __init__(self, atr='123'):
        self.attr = atr

    def __enter__(self):
        print(f'__enter__ in {self.__class__.__name__}', self.attr)
        return self

    def __exit__(self, *args):
        print(f'__exit__ on {self.__class__.__name__}', self.attr)


class Test1(Test):
    pass

test = Test('123456')


with test, Test1() as t1:
    pass
