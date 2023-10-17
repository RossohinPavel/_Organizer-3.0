def decorator(type_obj):
    old_mro = type_obj.__class__.mro(type_obj)
    def new_mro():
        return old_mro[:1] + [AnotherTest] + old_mro[1:]
    setattr(type_obj.__class__, 'mro', new_mro)
    return type_obj


class AnotherTest:
    attr = 0


@decorator
class Test:
    pass


print(AnotherTest.attr)