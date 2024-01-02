from ...source import *
from .stickergen_frame import StickerGenFrame


class InfoFrame(ttk.Frame):
    """Фрейм с отображением различной информации."""

    def __init__(self, master: Any) -> None:
        super().__init__(master)

        left = ttk.Frame(self, padding=(5, 5, 3, 5))
        left.place(x=0, y=0, relwidth=0.6, relheight=1)
        StickerGenFrame(left).pack(fill=ttkc.X)

        right = ttk.Frame(self, padding=(3, 5, 5, 5))
        right.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        self.draw_tracker_frame(right)
        self.draw_info_frame(right)
    
    def _draw_separator_frame(self, master: Any) -> ttk.Frame:
        """Вспомогательня ф-я для отрисовки фрема с черточкой в начале"""
        frame = ttk.Frame(master, padding=(15, 0, 0, 0))
        frame.pack(anchor=ttkc.W)
        ttk.Separator(frame, orient='horizontal').place(width=15, rely=0.44, x=-15)
        return frame
    
    def draw_tracker_frame(self, master: Any) -> None:
        """Отрисовка виджетов управления Трекером заказов"""
        HeaderLabel(master, text='Трекер заказов', anchor='n').pack(fill=ttkc.X, pady=(0, 2))
        self.draw_status_line(master)
        self.draw_tracker_mode_line(master)
        self.draw_log_depth_line(master)
        btn = ttk.Button(
            master, 
            style='minibtn.Outline.TButton',
            text='Ручное обновление',
            # command=None,
        )
        btn.pack(fill=ttkc.X, pady=10)
    
    def draw_status_line(self, master: Any) -> None:
        """Группа фреймов отображения статуса трекера"""
        ttk.Label(master, text='Статус:', style='minipadding.TLabel').pack(anchor=ttkc.W)
        frame = self._draw_separator_frame(master)
        status_var = ttk.StringVar(frame, value='Повтор в 11:25')
        ttk.Label(frame, text='Повтор в 11:25', style='minipadding.TLabel').pack(pady=(2, 0))
    
    def draw_tracker_mode_line(self, master: Any) -> None:
        """Отрисовка группы фреймов управления режимом трекера"""
        ttk.Label(master, text='Режим:', style='minipadding.TLabel').pack(anchor=ttkc.W, pady=(10, 0))
        frame = self._draw_separator_frame(master)
        var = ttk.IntVar(self)
        chbtn = ttk.Checkbutton(
            master=frame, 
            text='Автоматический', 
            style='success-round-toggle', 
            onvalue=1, 
            offvalue=0,
            variable=var,
            # command=init
            )
        chbtn.pack(anchor=ttkc.W, padx=(2, 0), pady=(2, 0))
    
    def draw_log_depth_line(self, master: Any) -> None:
        """Отрисовка группы фреймов управления глубиной проверки заказов"""
        ttk.Label(master, text='Глубина проверки:').pack(anchor=ttkc.W, pady=(10, 0))
        frame = self._draw_separator_frame(master)
        s = SettingLine(frame, None, _postfix='-  Заказов')
        s.pack(anchor=ttkc.W, padx=(2, 0))
        s._var.set(str(30))
    
    def draw_info_frame(self, master: Any) -> None:
        """Отрисовка кнопок информации"""
        lbl = HeaderLabel(master, text='Информация', anchor='n')
        lbl.pack(fill=ttkc.X, expand=1, anchor=ttkc.S)
        b1 = ttk.Button(
            master, 
            style='minibtn.Outline.TButton',
            text='Заказы', 
            # command=None
        )
        b1.pack(fill=ttkc.X, pady=(2, 5))
        b2 = ttk.Button(
            master, 
            style='minibtn.Outline.TButton',
            text='Клиенты', 
            command=lambda: print(b1.winfo_geometry())
        )
        b2.pack(fill=ttkc.X)
