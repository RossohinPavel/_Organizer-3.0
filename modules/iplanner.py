import threading
import time


__all__ = ('IPlanner', )


class IPlanner:
    """Планировщик, предоставляющий доступ для создания параллельных потоков для программы"""
    __instance = None
    __loops = []
    __lock = threading.Lock()

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __get_task(cls, func) -> callable:
        """Декоратор, возвращающий ф-ю обернутую в контекстный менеджер для последовательного выполнения задач"""
        def wrapper(*args, **kwargs):
            with cls.__lock:
                func(*args, **kwargs)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    @classmethod
    def create_task(cls, func: callable, args: tuple = (), kwargs: dict | None = None):
        """
        Создание задачи. Задача поставлена в очередь вызовов. Если очередь пуста, задача будет выполнена немедленно
        :param func: Cсылка на функцию
        :param args: Именованные аргументы к функции
        :param kwargs: Позиционные аргументы к функции
        """
        thread = threading.Thread(target=cls.__get_task(func), args=args, kwargs=kwargs)
        thread.start()

    @classmethod
    def create_loop(cls, func: callable, delay: int | float = 2, args: tuple = (), kwargs: dict | None = None):
        """
        Создание цикла, который будет регистрировать задачи в планировщики спустя задержку.
        Регистрация 1 задачи происходит немедленно. Последующие - по мере выполнения предыдущих.
        :param func: Ссылка на функцию
        :param delay: Задержка (в секундах), спустя которую необходимо повторять цилк
        :param args: Именованные аргументы к функции
        :param kwargs: Позиционные аргументы к функции
        """
        cls.__loops.append(Loop(func, delay, args, kwargs))


class Loop:
    """Класс для хранения информации о цикле и запуска его"""
    __reg_func = IPlanner.create_task

    def __init__(self, func, delay, args, kwargs):
        self.start = 0
        self.func = self.__endless_decorator(func)
        self.delay = delay
        self.args = args
        self.kwargs = kwargs
        self.__run_thread()

    def __endless_decorator(self, func):
        """Оборачиваем ф-ю в декоратор бесконечных вызовов. Цикл будет прерван с окночанием работы программы"""
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            self.__run_thread()
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    def __init_loop(self):
        """Отправляет в очередь функцию из цикла. Засыпает, если функция завершила свою работу раньше задержки"""
        delay = self.delay - (time.time() - self.start)
        if delay > 0:
            time.sleep(delay)
        self.start = time.time()
        self.__reg_func(self.func, self.args, self.kwargs)

    def __run_thread(self):
        """Запускает демонический поток выполнения"""
        demon_thread = threading.Thread(target=self.__init_loop, daemon=True)
        demon_thread.start()