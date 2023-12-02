from .._source import *


class MyMeter(tb.Meter):
    """Более удобный для меня метр виджет"""

    def __init__(self, master: Any, /, **kwargs):
        # Определяем основные настройки виджета
        super().__init__(
            master,
            metersize=160,
            textfont='-size 20 -weight bold',
            interactive=True,
            # stripethickness=0,    # 360 градусов максимальное значение, как в обычном круге. Значение должно быть int
            **kwargs
            )

    def _setup_widget(self):
        super()._setup_widget()
        self.meterframe.configure(height=int(self._metersize * 0.68))

    def _set_show_text(self):
        """Переопределенная ф-я для отрисовки основного счетчика внутри метер виджета"""
        super()._set_show_text()
        self.textframe.pack_forget()
        if self._showtext:
            if self._subtext:
                self.textframe.place(relx=0.5, rely=0.50, anchor='center')
            else:
                self.textframe.place(relx=0.5, rely=0.5, anchor='s')

    def _set_subtext(self):
        if self._subtextfont:
            if self._showtext:
                self.subtext.place(relx=0.5, rely=0.71, anchor='center')
            else:
                self.subtext.place(relx=0.5, rely=0.5, anchor='center')


class OperationMeter(MyMeter):
    """Метр виджет для отображения операций"""
    def __init__(self, master: Any, /, **kwargs):
        super().__init__(
            master,
            arcrange=210,
            arcoffset=165,
            bootstyle='info',
            textright='/ 5',
            # stripethickness=42,
            **kwargs
            )


class ProcessingFrame:
    """Конструктор для фрейма отображающего статус обработки различных задач. Используется как контекстный менеджер"""  
    def __init__(self, frame: tb.Labelframe):
        self.header = tb.StringVar(master=frame)
        self._header_label = tb.Label(master=frame, textvariable=self.header, anchor='w', width=22)
        self.operation = OperationMeter(frame, subtext='super_long_file_name')
        self.file = tb.Meter(frame, metersize=160, interactive=True, textfont='-size 18 -weight bold', subtext='long_file_name')
        self.__exit__()

    def __enter__(self) -> None:
        """При входе в менеджер, размещаем виджеты"""
        self._header_label.pack(pady=(0, 2))
        self.operation.pack()
        self.file.pack()

    def __exit__(self, *args) -> None:
        """При выходе - сбрасываем текстовые переменные и скрываем их виджеты"""
        self.header.set('__Имодуль__')
        self._header_label.pack_forget()
        self.operation.pack_forget()
        self.file.pack_forget()
