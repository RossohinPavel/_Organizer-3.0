import threading
import time


class Task(threading.Thread):
    def __init__(self, group=None, target=None, name=None, parallels=True, callback=None, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.parallels = parallels
        self.callback = callback
        self.status = 'created'

    def __run_callback(self):
        if self.callback:
            self.callback()

    def run(self):
        self.status = 'in_progress'
        self.__run_callback()
        super().run()
        self.__run_callback()
        self.status = 'finished'
        

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
        
    @classmethod
    def __check_loop_tasks(cls):
        pass

    @classmethod
    def __init_queue_tasks(cls):
        for task in cls.__queue:
            if task.status == 'created' and (task.parallels or (not task.parallels and not cls.__lock)):
                task.start()
                    
    @classmethod
    def __clear_queue(cls):
        print(cls.__queue)
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
        print(cls.__queue)
        cls.__alive = False

    @classmethod
    def reg_task(cls, func, parallels=True, args=(), kwargs=None):
        callback = None
        if not parallels:
            callback = IPlanner._lock_cb
        cls.__queue.append(Task(target=func, parallels=parallels, callback=callback, args=args, kwargs=kwargs))

    @classmethod
    def reg_loop(self, func, timer=0, args=None, kwargs=None, parallels=True):
        pass

def test_func():
    print('start')
    time.sleep(2)
    print('end')

planer = IPlanner()
time.sleep(1)
planer.reg_task(func=print, args=('\n1 time print', ))
planer.reg_task(func=test_func, parallels=False)
planer.reg_task(func=print, args=('\n1 time print', ))
planer.reg_task(func=test_func, parallels=False)
time.sleep(10)
planer.kill()
