from ...source import *


class TrackerFrame(ttk.Frame):
    """Фрейм для отображения статуса и работы с трекером заказов."""

    def __init__(self, master: Any, padding: int | tuple[int, ...]):
        super().__init__(master, padding=padding)   # type:  ignore

        lbl = HeaderLabel(self, text='Трекер заказов', anchor='n')
        lbl.pack(fill=ttkc.X, pady=(0, 3))

        self.draw_status_line()
        self.draw_tracker_mode_line()
        self.draw_log_depth_line()
        btn = ttk.Button(
            self, 
            style='minibtn.Outline.TButton',
            text='Ручное обновление',
            command=lambda: AppManager.ot.manual_init(),
        )
        btn.pack(fill=ttkc.X, pady=15)

    def _draw_separator_frame(self) -> ttk.Frame:
        """Вспомогательня ф-я для отрисовки фрема с черточкой в начале"""
        frame = ttk.Frame(self, padding=(15, 0, 0, 0))
        frame.pack(anchor=ttkc.W)

        s = ttk.Separator(frame, orient='horizontal')
        s.place(width=12, rely=0.44, x=-12)

        return frame

    def draw_status_line(self) -> None:
        """Группа фреймов отображения статуса трекера"""
        lbl = ttk.Label(self, text='Статус:', style='minipadding.TLabel')
        lbl.pack(anchor=ttkc.W, pady=(0, 3))

        frame = self._draw_separator_frame()
        lbl = ttk.Label(frame, style='minipadding.TLabel')
        lbl.pack()
        AppManager._desc.ot_status.add_call(lambda v: lbl.configure(text=v))    #type: ignore

    def draw_tracker_mode_line(self) -> None:
        """Отрисовка группы фреймов управления режимом трекера"""
        def change_text(v: int) -> None:
            """Меняет название на виджете Checkbutton"""
            chbtn.configure(text='Автоматический' if v == 1 else 'Ручной')

        lbl = ttk.Label(self, text='Режим:', style='minipadding.TLabel')
        lbl.pack(anchor=ttkc.W, pady=(10, 0))

        frame = self._draw_separator_frame()
        var = ttk.IntVar(self)
        chbtn = ttk.Checkbutton(
            master=frame, 
            style='success-round-toggle', 
            onvalue=1, 
            offvalue=0,
            variable=var,
            command=lambda: setattr(AppManager.stg, 'autolog', var.get())
            )
        chbtn.pack(anchor=ttkc.W, padx=(2, 0), pady=(2, 0))
        AppManager._desc.autolog.add_call(var.set)              #type: ignore
        AppManager._desc.autolog.add_call(change_text)          #type: ignore

    def draw_log_depth_line(self) -> None:
        """Отрисовка группы фреймов управления глубиной проверки заказов"""
        lbl = ttk.Label(self, text='Глубина проверки:')
        lbl.pack(anchor=ttkc.W, pady=(10, 0))

        frame = self._draw_separator_frame()
        s = SettingLine(frame, self._change_log_check_depth, _postfix='-  Заказов')
        s.pack(anchor=ttkc.W, padx=(2, 0))

        AppManager._desc.log_check_depth.add_call(s._var.set)   #type: ignore

    def _change_log_check_depth(self) -> None:
        """Запрос на изменения настроек."""
        res = Querybox.get_integer(
            parent=self,
            title='Глубина проверки',
            prompt='Введите новое значение:',
            initialvalue=AppManager.stg.log_check_depth,
            minvalue=0
        )
        if isinstance(res, int): 
            AppManager.stg.log_check_depth = res
