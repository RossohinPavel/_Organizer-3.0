from gui._source import *


class InitSampleWindow(ChildWindow):
    """Вспомогательное окно для заполнения переменных в текстовом шаблоне"""
    # Параметр height используется как множитель для растягивания окна
    WIN_GEOMETRY = Geometry(230, 54)
    LIN_GEOMETRY = Geometry(230, 54)

    def __init__(self, master: Any, title: str, text: str) -> None:
        self._title = title
        self._text = text.split('?%')
        self._widgets = []
        super().__init__(AppManager.mw, 
                        relief='solid',
                        overrideredirect=True,
                        border=1
                        )
        self._widgets[0].focus_set()
        self.bind('<Return>', self.create_sample)

    def get_geometry_by_system(self) -> Geometry:
        old = super().get_geometry_by_system()
        return Geometry(old.width, 59 + len(self._text[1::2]) * old.height)
    
    def main(self, **kwargs) -> None:
        ttk.Label(master=self, text='Заполните поля:').pack(pady=(1, 0))
        for var in self._text[1::2]:
            ttk.Label(master=self, text=var).pack(padx=(5, 0), pady=(1, 0), anchor='nw')
            entry = ttk.Entry(master=self, width=30)
            entry.pack(padx=2, pady=(1, 0), expand=1, fill='x')
            self._widgets.append(entry)
        ttk.Button(self, text='Ок', width=8, command=self.create_sample).pack(side='left', padx=2, pady=2)
        ttk.Button(self, text='Отмена', width=8, command=self.destroy).pack(side='right', pady=2, padx=(0, 2))

    def create_sample(self, event: tkinter.Event | None = None):
        """Создание сэмпла и помещение его в буфер обмена"""
        def generator():
            for i, v in enumerate(self._text):
                if i % 2 == 1:
                    yield self._widgets[(i - 1) // 2].get()
                else:
                    yield v
        self.master.clipboard_clear()
        self.master.clipboard_append(''.join(generator()))
        self.destroy()
        tkmb.showinfo(title=self._title, message='Шаблон скопирован в буфер обмена.')
