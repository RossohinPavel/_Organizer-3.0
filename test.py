class Test:
    __slots__ = 'connect', 'cursor'

    def __new__(cls, db_name):
        if not getattr(cls, db_name, None):
            setattr(cls, db_name, 'succes')
        return super().__new__(cls)


test = Test('app')
test3 = Test('app')
test2 = Test('stg')

print(test2.__dict__)