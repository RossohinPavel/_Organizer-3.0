from gui._source import *


class InitSampleWindow(ChildWindow):
    """Вспомогательное окно для заполнения переменных в текстовом шаблоне"""
    width = 194

    def __init__(self, *args, **kwargs) -> None:
        self.text = kwargs.pop('text').split('?%')
        self.sample_title = kwargs.pop('sample_title')
        self.height = 20 + 30 + len(self.text[1::2]) * 44
        self.widget_lst = []
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.config(border=1, relief='solid')
        self.widget_lst[0].focus_set()
        self.bind('<Return>', self.create_sample)

    def main(self, *args, **kwargs) -> None:
        ttk.Label(master=self, text='Заполните поля:').pack(pady=(1, 0))
        for var in self.text[1::2]:
            ttk.Label(master=self, text=var).pack(padx=(5, 0), pady=(1, 0), anchor='nw')
            entry = ttk.Entry(master=self, width=30)
            entry.pack(padx=2, pady=(1, 0), expand=1, fill='x')
            self.widget_lst.append(entry)
        MyButton(master=self, text='Ввод', width=8, command=self.create_sample).pack(side='left', padx=2, pady=2)
        MyButton(master=self, text='Закрыть', width=8, command=self.destroy).pack(side='right', pady=2, padx=(0, 2))

    def create_sample(self, event: tk.Event):
        """Создание сэмпла и помещение его в буфер обмена"""
        for i in range(len(self.widget_lst)):
            self.text[i * 2 + 1] = self.widget_lst[i].get()
        text = ''.join(self.text)
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.destroy()
        tkmb.showinfo(parent=self.master, title=self.sample_title, message='Шаблон скопирован в буфер обмена')
