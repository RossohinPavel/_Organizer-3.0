from threading import Thread, Lock
from typing import Callable, Any, Iterable, Mapping, Type
from .gui._source import tkmb
from .app_manager import AppManager


__all__ = ('TaskManager', )


class TaskManager:
    """Планировщик, предоставляющий доступ для создания параллельных потоков для программы"""
    __slots__ = '__lock'

    def __init__(self) -> None:
        self.__lock = Lock()

    def __get_task(self, func: Callable[[Any], None]) -> Type[Callable[[Any], None]]:
        """Замыкание, возвращающее ф-ю обернутую в контекстный менеджер для последовательного выполнения задач"""
        def wrapper(*args: Any, **kwargs: Mapping[str, Any]):
            AppManager.txtvars.queue.set(AppManager.txtvars.queue.get() + 1)
            with self.__lock, AppManager.pi:
                try:
                    func(*args, **kwargs)
                except Exception as exc:
                    tkmb.showerror('Ошибка', message=f'{repr(exc)}')
                    raise exc
            AppManager.txtvars.queue.set(AppManager.txtvars.queue.get() - 1)
        wrapper.__name__, wrapper.__doc__ = func.__name__, func.__doc__
        return wrapper

    def create_task(self, func: Type[Callable[[Any], None]], *args: Iterable[Any], **kwargs: Mapping[str, Any]) -> None:
        """Создание задачи. Задача будет поставлена в очередь вызовов. Если очередь пуста, задача запустится немедленно."""
        Thread(target=self.__get_task(func), args=args, kwargs=kwargs, daemon=True).start()
