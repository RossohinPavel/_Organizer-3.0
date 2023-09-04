class Manager1:
    def __enter__(self):
        print('start1')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('end1')


class Manager2:
    def __enter__(self):
        print('start2')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('end2')


def some_func():
    print('do_something')


with Manager1(), Manager2():
    some_func()
