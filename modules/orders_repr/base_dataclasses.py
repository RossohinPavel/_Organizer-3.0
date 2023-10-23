from dataclasses import dataclass, field


__all__ = ('Order', 'Edition', 'Photo')


@dataclass
class Order:
    """Датакласс для хранения информации о заказе"""
    name: str
    creation_date: str
    customer_name: str = 'Unknown'
    customer_address: str = 'Unknown'
    price: int = 0
    photo: tuple = field(default_factory=tuple)
    content: tuple = field(default_factory=tuple)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.name)


@dataclass
class Edition:
    """Датакласс для хранения информации о тиражах"""
    order_name: str
    name: str
    covers: int = 0
    pages: int = 0
    ccount: str = None
    comp: str = None

    def __hash__(self):
        return hash(self.name)


@dataclass
class Photo:
    """Датакласс для хранения информации о фотопечати в заказе"""
    order_name: str
    name: str
    count: int = 0
