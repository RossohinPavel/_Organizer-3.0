class Test:
    def __init__(self) -> None:
        self._mode = 0
        self.inner_attr = 'test'

    @property
    def mode(self) -> int:
        return self._mode
    
    @mode.setter
    def mode(self, value: int):
        self._mode = value
        print(self.inner_attr)


t = Test()


class Test2:
    def __init__(self) -> None:
        self.attr = t.mode


test2 = Test2()

test2.attr = 1