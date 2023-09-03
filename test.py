import threading
import time


class IPlanner:
    __instance = None
    __alive = True
    __main_thread = None
    __loop = ()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__main_thread = threading.Thread(target=cls.__run_main_thread)
            cls.__main_thread.start()
        return cls.__instance

    @classmethod
    def __run_main_thread(cls):
        while cls.__alive:
            for task in cls.__loop:
                task.start()
            time.sleep(1 - time.time() % 1)

    @classmethod
    def kill(cls):
        cls.__alive = False

    @classmethod
    def create_task(cls, func, loop=0, parallels=True, callbacks=(), args=(), kwargs=None):
        def inner(*args):
            task = Task(*args)
            task.start()
            if loop > 0:
                cls.__loop += (task, )

        threading.Thread(target=inner, args=(func, loop, parallels, callbacks, args, kwargs)).start()


class CallBack:
    __slots__ = 'func', 'pos', 'args', 'kwargs'

    def __init__(self, func, pos='both', args=(), kwargs=None):
        self.func = func
        self.pos = (pos, ) if pos != 'both' else ('before', 'after')
        self.args = args
        self.kwargs = kwargs if kwargs else {}

    def __call__(self, pos):
        if pos in self.pos:
            self.func(*self.args, **self.kwargs)


class Task:
    def __init__(self, func, delay, parallels, callbacks, args, kwargs):
        self.func = func
        self.delay = delay
        self.__timer = 0
        self.parallels = parallels
        self.callbacks = callbacks
        self.args = args
        self.kwargs = kwargs if kwargs else {}

    def start(self):
        if self.__timer == 0:
            self.__timer = self.delay
            thread = MyThread(self.func, self.callbacks, self.args, self.kwargs)
            thread.start()
        else:
            self.__timer -= 1


class MyThread(threading.Thread):
    def __init__(self, target, callbacks, args, kwargs):
        super().__init__(target=target, args=args, kwargs=kwargs)
        self._callbacks = callbacks

    def __run_callbacks(self, pos):
        for call in self._callbacks:
            call(pos)

    def run(self):
        self.__run_callbacks('before')
        super().run()
        self.__run_callbacks('after')


planner = IPlanner()
planner.create_task(print, args=('test_print', ), callbacks=(CallBack(print, pos='before', args=('-')), ))
planner.create_task(print, args=('test_print', ), callbacks=(CallBack(print, pos='after', args=('-')), ))
time.sleep(11)
planner.kill()
