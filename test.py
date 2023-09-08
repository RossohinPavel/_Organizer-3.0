class Property:
    attr = 'property'
    
    def __new__(cls, category, default_values):
        return cls.attr, cls.add_defaults(category)

    @staticmethod
    def add_defaults(category):
        return ''


class Product:
    propertys = (Property, )
    def __new__(cls, default_values):
        return dict(prop(cls, default_values) for prop in cls.propertys)

class Photobook(Product):
    pass
        

class ProductGenerator:
    __prd_dct = {'Photobook': Photobook}
    
    classmethod
    def create(cls, category, default_values=False):
        return cls.__prd_dct[category](default_values)


test = ProductGenerator()

print(test.create('Photobook', True))
