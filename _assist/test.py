from typing import NamedTuple


class Test(NamedTuple):
    def some_method(self):
        pass


class Subproduct(Test):
    """Сувенирная, сопровождающая продукция"""
    full_name: str                # Полное имя продукта
    segment: str                  # Общие особенности продукта
    short_name: str
    cover_print_mat: str          # Печатный материал


test = Subproduct('q', 'q', 'q', 'q')

print(test.__dict__)