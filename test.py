class Test1:
    atr = None


class Test2(Test1):
    def __init__(self):
        Test1.atr = self


test = Test2()

print(test.atr.atr)
