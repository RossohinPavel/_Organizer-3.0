class Descriptor:

    def __set_name__(self, owner, name):
        print(owner)
        self.__dict__[owner] = name
        print(self)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.__value

    def __set__(self, instance, value):
        self.__value = value
        instance.__dict__[self.__dict__[instance.__class__.__name__]] = value


class Test:
    auto_run = Descriptor()


t1 = Test()


class Test2:

    def __init__(self):
        self.another_name = t1.name


t2 = Test2()

print(t2.another_name)