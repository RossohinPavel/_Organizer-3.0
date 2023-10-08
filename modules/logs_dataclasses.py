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


@dataclass
class Edition:
    """Датакласс для хранения информации о тиражах"""
    order_name: str
    name: str
    covers: int = 0
    pages: int = 0
    ccount: str = None
    comp: str = None


@dataclass
class Photo:
    """Датакласс для хранения информации о фотопечати в заказе"""
    order_name: str
    name: str
    count: int = 0
