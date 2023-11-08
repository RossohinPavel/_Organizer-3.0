from threading import Thread, Lock
from typing import Callable, Any, Iterable, Mapping, Self

from .windows.frames.processing_frame import ProcessingFrame
from .windows.source import tkmb


__all__ = ('TaskManager', )


class TaskManager:
    """Планировщик, предоставляющий доступ для создания параллельных потоков для программы"""
    __instance = None
    __lock = Lock()
    __pf = ProcessingFrame()

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def __get_task(cls, func: Callable):
        """Декоратор, возвращающий ф-ю обернутую в контекстный менеджер для последовательного выполнения задач"""
        def wrapper(*args, **kwargs):
            cls.__pf.queue.set(cls.__pf.queue.get() + 1)
            with cls.__lock, cls.__pf:
                try:
                    func(*args, **kwargs)
                except Exception as exc:
                    tkmb.showerror('Ошибка', message=str(exc))
            cls.__pf.queue.set(cls.__pf.queue.get() - 1)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    @classmethod
    def create_task(cls, func: Callable[..., Any], args: Iterable[Any], kwargs: Mapping[str, Any] | None) -> None:
        """Создание задачи. Задача будет поставлена в очередь вызовов. Если очередь пуста, задача запустится немедленно."""
        Thread(target=cls.__get_task(func), args=args, kwargs=kwargs, daemon=True).start()
