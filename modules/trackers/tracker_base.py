from threading import Thread, Lock
from time import sleep
from modules.app_manager import AppManagerR


class TBase(AppManagerR):
    """Абстрактный класс реализующий общую логику работы трекера"""
    delay = 180

    def __init__(self):
        self.thread_dct = {}

    def run(self):
        """Абстрактная ф-я. В дочернем классе должна собирать в себе функции, реализующие логику работы трекера."""
        raise Exception('Функция run не переопределена в дочерном классе')

    def manual(self):
        """Абстрактная ф-я. В дочернем классе предоставляет возможность ручного запуска трекера и реализует соответствующую логику"""
        raise Exception('Функция run не переопределена в дочерном классе')

    def start_auto_tracking(self):
        self.thread_dct[MyThread(self)] = True

    def stop_auto_tracking(self):
        key = None
        for key, value in self.thread_dct.items():
            if not value:
                self.thread_dct[key] = False
                break
        del self.thread_dct[key]
    


class MyThread(Thread):
    def __init__(self, tracker):
        self.tracker = tracker
        super().__init__(daemon=True)

    def run(self):
        while self.tracker.thread_dct[self]:
            pass
            
        

    
