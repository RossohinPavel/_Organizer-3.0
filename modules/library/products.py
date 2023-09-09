from properties import *


class Product:
    main_prop = (full_name, segment, short_name)
    properties = ()

    def __init__(self, default_values=False):
        for prop in (*self.main_prop, *self.properties):
            prop(self, default_values)

    def category(self):
        return self.__class__.__name__


class Photobook(Product):
    pass


test = Photobook(True)
print(test.__dict__)
