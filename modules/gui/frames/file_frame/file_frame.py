from ...source import *
from .queue_frame import QueueFrame
from .processing_frame import ProcessingFrame


class FileFrame(ttk.Frame):
    """
        Фрейм отображающий статус обработки файлов. 
        Содержит кнопки запуска обработки.
    """

    def __init__(self, master: Any) -> None:
        super().__init__(master, padding=5)

        # Отображение очереди задач
        AppManager.queue = queue = QueueFrame(self)
        queue.pack(fill=ttkc.X)

        # Отображение фрейма статуса обработки
        AppManager.pf = pf = ProcessingFrame(self)
        pf.pack(fill=ttkc.X, padx=5, pady=(0, 15))

        pf.__exit__()
        pf.__enter__()

        left = ttk.Frame(self)
        left.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1, padx=(0, 3))
        self.draw_left_column(left)

        center = ttk.Frame(self)
        center.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1, padx=(3, 3))
        self.draw_center_column(center)

        right = ttk.Frame(self)
        right.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1, padx=(3, 0))
        self.draw_right_column(right)
    
    def draw_left_column(self, master: Any) -> None:
        """Отрисовка виджетов в левом столбике"""
        HeaderLabel(master, text='Целевая обработка', padx=17).place(x=0, y=0, relwidth=1)

        btn1 = ttk.Button(
            master, 
            text='Разметка обложек', 
            # command=lambda: CoverMarkerWindow(self), 
            )
        btn2 = ttk.Button(
            master, 
            text='Раскодировка', 
            # command=lambda: PageDecoderWindow(master=self), 
            )
        btn3 = ttk.Button(
            master, 
            text='Направляющие', 
            # command=lambda:, 
            )
        btn4 = ttk.Button(
            master, 
            text='Холсты', 
            # command=lambda:, 
            )
        for i, widget in enumerate((btn1, btn2, btn3, btn4)):
            widget.configure(style='minibtn.Outline.TButton')
            widget.place(x=0, relwidth=1, y=20 + i * 30)

    def draw_center_column(self, master: Any) -> None:
        """Отрисовка виджетов в центральном столбике"""
        HeaderLabel(master, text='Файлы заказа', padx=32).place(x=0, y=0, relwidth=1)

        btn1 = ttk.Button(
            master, 
            text='Замена', 
            # command=lambda:, 
            )
        btn2 = ttk.Button(
            master, 
            text='Восстановление', 
            # command=lambda:, 
            )
        for i, widget in enumerate((btn1, btn2)):
            widget.configure(style='minibtn.Outline.TButton')
            widget.place(x=0, relwidth=1, y=20 + i * 30)

    def draw_right_column(self, master: Any) -> None:
        """Отрисовка виджетов в правом столбике"""
        HeaderLabel(master, text='Дополнительно', padx=28).place(x=0, y=0, relwidth=1)

        btn1 = ttk.Button(
            master, 
            text='Роддом', 
            # command=lambda:, 
            )

        for i, widget in enumerate((btn1, )):
            widget.configure(style='minibtn.Outline.TButton')
            widget.place(x=0, relwidth=1, y=20 + i * 30)