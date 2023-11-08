from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from test import Test


class Test1:
    def test1_method(self):
        print('call')
        return