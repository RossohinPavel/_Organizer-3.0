__all__ = ('Order', 'Edition', 'PhotoEdition', 'OrderInfo')


class Order:
    """Датакласс для описания заказа"""
    __slots__ = 'name', 'creation_date', 'path', 'photo', 'order_info', 'content'

    def __init__(self, path, creation_date, name):
        self.name = name
        self.creation_date = creation_date
        self.path = f'{path}/{creation_date}/{name}'
        self.photo = None
        self.order_info = None
        self.content = tuple()


class Edition:
    """Датакласс для хранения информации о тиражах"""
    __slots__ = 'name', 'matrix_repr'

    def __init__(self, name):
        self.name = name
        self.matrix_repr = {}


class PhotoEdition:
    """Датакласс для хранения информации о фотопечати в заказе"""
    __slots__ = 'matrix_repr'

    def __init__(self):
        self.matrix_repr = {}


class OrderInfo:
    """Датакласс для описания сопутствубщей информации о заказе"""
    __slots__ = 'customer_name', 'customer_address', 'price'

    def __init__(self):
        self.customer_name = 'unknown'
        self.customer_address = 'unknown'
        self.price = 0
