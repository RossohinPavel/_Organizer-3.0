from typing import TYPE_CHECKING
from collections import namedtuple


if not TYPE_CHECKING:
    from test1 import Test1


class Test:
    app: Test1 | None = None


Test.app = Test1()


def some_func():
    Test.app.test1_method()

some_func()