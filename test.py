class Test:
    __slots__ = ('one', 'two')

    def __init__(self):
        self.one = 1
        self.two = 2


test = Test()

print(test.__slots__)