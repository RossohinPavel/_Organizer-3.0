class Descriptor:
    __slots__ = '_name', 'set_callback'

    def __set_name__(self, owner, name):
        self._name = name

    def __init__(self, set_callback=()):
        self.set_callback = set_callback


class TestClass:
    attr = Descriptor()


test = TestClass()
test.attr = 1

print(test.attr)