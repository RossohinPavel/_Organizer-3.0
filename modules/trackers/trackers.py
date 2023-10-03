from modules.app_manager import AppManagerW


class Trackers(AppManagerW):
    """Класс, собирающий в себе остальные трекеры и предоставляющий к ним доступ"""
    _alias = 'trs'
    __slots__ = 'ot'
    
    def __init__(self):
        self.ot = None
