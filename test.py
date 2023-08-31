import threading
import time


class Task:
    def __init__(self, func, args=None, kwargs=None):
        self.func = func
        self.args = args if args else ()
        self.kwargs = kwargs if kwargs else {}
        self.status = 'created'
        self._thread = None

    def run(self):
        if self._thread is None:
            self.status = 'in_progress'
            self._thread = threading.Thread(target=self.func, args=self.args, kwargs=self.kwargs)
            self._thread.start()
        self.after_run()

    def after_run(self): pass

    def __bool__(self):
        return self.status != 'finished'


class ParallelTask(Task):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__delay = 5
        self.__timer = self.__delay

    def after_run(self):
        if self.__timer > 0:
            self.__timer -= 1
        elif self.__timer <= 0 and not self._thread.is_alive():
            self._thread = None
            self.__timer = self.__delay


class ConsistentTask(Task):
    def after_run(self):
        if not self._thread.is_alive():
            self.status = 'finished'


class IPlanner:
    __alive = False

    def __init__(self):
        self._queue = []
        self.__thread = threading.Thread(target=self.__run_main_thread)

    def __run_main_thread(self):
        while self.__alive:
            for task in self._queue:
                task.run()
                if not task:
                    self._queue.remove(task)
            time.sleep(1)

    def reg(self, func, args=None, kwargs=None, parallels=False):
        if parallels:
            self._queue.append(ParallelTask(func, args, kwargs))
        else:
            self._queue.append(ConsistentTask(func, args, kwargs))
        if not self.__alive:
            self.__alive = True
            self.__thread.start()

    def kill(self):
        self.__alive = False


planer = IPlanner()

planer.reg(print, ('Я принтуюсь каждые 5 секунд', ), parallels=True)
planer.reg(print, ('Я должен принтануться всего 1 раз', ))
time.sleep(10)
planer.reg(print, ('Я должен принтануться всего 1 раз', ))
print(planer._queue)
time.sleep(5)
print(planer._queue)
time.sleep(6)
planer.kill()
