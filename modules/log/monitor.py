import threading as th

__all__ = ('Monitor', )


class Monitor:
    """Основной объект слежения за файлами"""
    __instance = None
    __orders = []

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, settings, txt_vars=None):
        self.settings = settings
        self.txt_vars = txt_vars

    def __main(self):
        print('wake up!')

    def run(self):
        th1 = th.Thread(target=self.__main)
        th1.start()
