from ..source import *
from ...mail_samples import MailSamples


class MailSamplesFrame(LabeledFrame):
    _samples = MailSamples()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Текстовые шаблоны', **kwargs)
        self.listbox = None
        self.headers = self._samples.get_headers()
        self.listbox_values = tk.Variable(master=self, value=self.headers)
        self.show_main_widget()

    def show_main_widget(self):
        self.listbox = tk.Listbox(master=self.container, listvariable=self.listbox_values)
        self.listbox.pack(expand=1, fill='both', side='left')
        scroll = ttk.Scrollbar(master=self.container, command=self.listbox.yview)
        scroll.pack(side='right', fill='y')
        self.listbox.config(yscroll=scroll.set)
        self.listbox.bind('<Double-Button-1>', self.init_sample)

    def init_sample(self, event):
        sample = self.headers[self.listbox.curselection()[0]]
        text = self._samples.get_sample(sample)
        if len(text) == 1:
            self.clipboard_clear()
            self.clipboard_append(text[0])
            tkmb.showinfo(parent=self, title=sample, message='Шаблон скопирован в буфер обмена')
        else:
            InitSampleWindow(master=self.master.master.master, text=text, sample=sample)


class InitSampleWindow(ChildWindow):
    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text')
        self.sample = kwargs.pop('sample')
        self.width, self.height = 194, len(self.text[1::2]) * 94
        self.widget_lst = []
        super().__init__(*args, **kwargs)
        self.overrideredirect(True)
        self.config(border=1, relief='solid')
        self.widget_lst[0].focus_set()
        self.bind('<Return>', self.create_sample)

    def main(self, *args, **kwargs):
        ttk.Label(master=self, text='Заполните поля:').pack(pady=(1, 0))
        for var in self.text[1::2]:
            ttk.Label(master=self, text=var).pack(padx=(5, 0), pady=(1, 0), anchor='nw')
            entry = ttk.Entry(master=self, width=30)
            entry.pack(padx=2, pady=(1, 0), expand=1, fill='x')
            self.widget_lst.append(entry)
        MyButton(master=self, text='Ввод', width=8, command=self.create_sample).pack(side='left', padx=2, pady=2)
        MyButton(master=self, text='Закрыть', width=8, command=self.destroy).pack(side='right', pady=2, padx=(0, 2))

    def create_sample(self, event=None):
        for i in range(len(self.widget_lst)):
            self.text[i*2+1] = self.widget_lst[i].get()
        text = ''.join(self.text)
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.destroy()
        tkmb.showinfo(parent=self.master, title=self.sample, message='Шаблон скопирован в буфер обмена')
