from modules.app_manager import AppManagerW
from modules.trackers.orders_tracker import OrdersTracker


class Trackers(AppManagerW):
    """Класс, собирающий в себе остальные трекеры и предоставляющий к ним доступ"""
    _alias = 'tr'
    __slots__ = 'ot'
    
    def __init__(self):
        self.ot = OrdersTracker()
