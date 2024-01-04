"""
    Собирает в себя различные классы и объекты, которые используются для типизации программы
"""

from typing import (
    Any,
    Callable,
    Iterator,
    Literal,
    NamedTuple,
    NoReturn,  
    Type,
    TYPE_CHECKING,
    TypeVar,  
    Self
)
from .data_base.library.products import Categories
from .data_base.log import Order, Edition