from threading import Thread, Lock
from .app_manager import AppManager
from .windows.source import tkmb


__all__ = ('TaskManager', )


class TaskManager(AppManager):
    """Планировщик, предоставляющий доступ для создания параллельных потоков для программы"""
    _alias = 'tm'
    __lock = Lock()

    @classmethod
    def __get_task(cls, func: callable) -> callable:
        """Декоратор, возвращающий ф-ю обернутую в контекстный менеджер для последовательного выполнения задач"""
        def wrapper(*args, **kwargs):
            with cls.app_m.pf, cls.__lock:
                cls.app_m.pf.queue.set(cls.app_m.pf.queue.get() + 1)
                try:
                    func(*args, **kwargs)
                except Exception as exc:
                    tkmb.showerror('Ошибка', message=exc)
                cls.app_m.pf.queue.set(cls.app_m.pf.queue.get() - 1)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    @classmethod
    def create_task(cls, func: callable, args: tuple = (), kwargs: dict | None = None):
        """Создание задачи. Задача будет поставлена в очередь вызовов. Если очередь пуста, задача запустится немедленно.
        :param func: Cсылка на функцию
        :param args: Именованные аргументы к функции
        :param kwargs: Позиционные аргументы к функции"""
        Thread(target=cls.__get_task(func), args=args, kwargs=kwargs, daemon=True).start()
