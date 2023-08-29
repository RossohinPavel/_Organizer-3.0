class Monitor:
    """Основной объект слежения за файлами"""
    __instance = None
    __orders = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__()
        return cls.__instance

    def __init__(self, settings, txt_vars):
        self.settings = settings
        self.txt_vars = txt_vars
