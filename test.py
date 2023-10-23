class Test:
    __slots__ = 'test'

    def __init__(self):
        self.test = 1


class Test1(Test):
    __slots__ = ()

    def __init__(self):
        self.test = 2

t = Test1()
print(t.test.__dict__)