from ...source import *
from ....descriptors import FileQueue


class FileFrame(ttk.Frame):
    """
        Фрейм отображающий статус обработки файлов. 
        Содержит кнопки запуска обработки
    """
    queue = FileQueue

    def __init__(self, master: Any) -> None:
        super().__init__(master, padding=5)
        
        # Отображение очереди задач
        FileQueue.add_call(self.queue_cofigure)
        self.queue_lbl = HeaderLabel(self)
        self.queue_lbl.pack(fill=ttkc.X)
        self.queue = 0
    
    def queue_cofigure(self, value: int) -> None:
        """Связанная с дескриптором ф-я, изменяющая статус количества задач в очереди"""
        self.queue_lbl.lbl.configure(text=f'Задач в очереди: {value}')


