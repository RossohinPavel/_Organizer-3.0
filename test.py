import threading
import time


__all__ = ('IPlanner', 'CallBack')


class IPlanner:
    __instance = None
    __alive = True
    __lock = False
    __main_thread = None
    __queue = []
    __loop = []

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__main_thread = threading.Thread(target=cls.__run_main_thread)
            cls.__main_thread.start()
        return cls.__instance

    @classmethod
    def __run_main_thread(cls):
        while cls.__alive:
            start = time.time()
            cls.__check_loop_tasks()
            cls.__init_queue_tasks()
            cls.__clear_queue()
            time.sleep(1 - (time.time() - start))

    @classmethod
    def _lock_cb(cls):
        cls.__lock = not cls.__lock


    @staticmethod
    def __check_callbacks(callbacks):
        if not isinstance(callbacks, tuple):
            callbacks = (callbacks, )
        for call in callbacks:
            if not isinstance(call, CallBack):
                raise Exception(f'Функция {call} не обернута в CallBack')
        return callbacks
        
    @classmethod
    def __check_loop_tasks(cls):
        for loop in cls.__loop:
            loop()

    @classmethod
    def __init_queue_tasks(cls):
        for task in cls.__queue:
            if task.status == 'created' and (task.parallels or (not task.parallels and not cls.__lock)):
                task.start()
                    
    @classmethod
    def __clear_queue(cls):
        if not cls.__queue:
            return
        ind = 0
        while ind < len(cls.__queue):
            if cls.__queue[ind].status == 'finished':
                del cls.__queue[ind]
            else:
                ind += 1

    @classmethod
    def kill(cls):
        cls.__alive = False

    @classmethod
    def reg_task(cls, func, parallels=True, callbacks=(), args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        callbacks = cls.__check_callbacks(callbacks)
        if not parallels:
            callbacks = (CallBack(cls._lock_cb), *callbacks)
        cls.__queue.append(Task(target=func, args=args, kwargs=kwargs, parallels=parallels, callbacks=callbacks))

    @classmethod
    def reg_loop(cls, func, timer=0, parallels=True,  callbacks=(), args=(), kwargs=None):
        cls.__loop.append(Loop(func, timer, parallels, callbacks, args, kwargs))        


class CallBack:
    __slots__ = 'func', 'pos', 'args', 'kwargs'
    
    def __init__(self, func, pos='both', args=(), kwargs=None):
        self.func = func
        self.pos = self.__get_position(pos)
        self.args = args
        self.kwargs = kwargs if kwargs else {}

    @staticmethod
    def __get_position(pos):
        if pos not in ('both', 'before', 'after'):
            pos = ()
        return ('before', 'after') if pos == 'both' else (pos, )

    def __call__(self, pos):
        if pos in self.pos:
            self.func(*self.args, **self.kwargs)


class Loop:
    __reg_func = IPlanner.reg_task
    __slots__ = ('func', 'timer', '__delay', 'parallels', 'callbacks', 'args', 'kwargs')
    
    def __init__(self, func, timer, parallels, callbacks, args, kwargs):
        self.func = func
        self.timer = timer
        self.__delay = 0
        self.parallels = parallels
        self.callbacks = callbacks
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        if self.__delay == 0:
            self.__delay = self.timer
            self.__reg_func(self.func, self.parallels, self.callbacks, self.args, self.kwargs)
        self.__delay -= 1


class Task(threading.Thread):
    def __init__(self, target, args, kwargs, parallels, callbacks, group=None, name=None):
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.parallels = parallels
        self.status = 'created'
        self.callback = callbacks
        
    def __run_callback(self, pos):
        for call in self.callback:
            call(pos)

    def run(self):
        self.status = 'in_progress'
        self.__run_callback('before')
        super().run()
        self.__run_callback('after')
        self.status = 'finished'
