from typing import Any
from dataclasses import dataclass, field


__all__ = ('OrderDC', 'EditionDC', 'PhotoDC')


@dataclass
class OrderDC:
    """"""
    name: str
    creation_date: str
    customer_name: str = 'Unknown'
    customer_address: str = 'Unknown'
    price: float = 0
    photo: list = field(default_factory=list)
    content: list = field(default_factory=list)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.name == other
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        return hash(self.name)


@dataclass
class EditionDC:
    """"""
    name: str
    covers: int = 0
    pages: int = 0
    ccount: str | None = None
    comp: str | None = None


@dataclass
class PhotoDC:
    """"""
    name: str
    count: int = 0
