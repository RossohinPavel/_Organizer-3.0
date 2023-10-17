from ..app_manager import AppManager
from .orders_tracker import OrdersTracker


__all__ = ('init_trackers', )


def init_trackers():
    # Собираем трекеры в 1 переменной
    trackers = AppManager.create_group('Trackers', 'tr')
    trackers.ot = OrdersTracker()
