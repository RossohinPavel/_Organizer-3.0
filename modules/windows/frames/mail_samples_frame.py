from ..source import *
from ...mail_samples import MailSamples


class MailSamplesFrame(LabeledFrame):
    """Фрейм для работы с текстовыми шаблонами"""
    _samples = MailSamples()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Текстовые шаблоны', **kwargs)
        self.listbox = ttk.Treeview(master=self.container, show='tree')
        self.show_main_widget()
        self.update_listbox()

    def show_main_widget(self):
        """Отрисовка основных виджетов"""
        self.listbox.pack(expand=1, fill='both', side='left')
        scroll = ttk.Scrollbar(master=self.container, command=self.listbox.yview)
        scroll.pack(side='right', fill='y')
        self.listbox.config(yscroll=scroll.set)
        self.listbox.bind('<Double-Button-1>', self.init_sample)
        self.listbox.bind('<Return>', self.init_sample)
        self.listbox.bind('<Button-3>', self.rclick_event)

    def update_listbox(self):
        """Наделение листобокса именами текстовых шаблонов"""
        for i in self.listbox.get_children(''):
            self.listbox.delete(i)
        for i, v in enumerate(self._samples.get_headers()):
            self.listbox.insert('', 'end', id=str(i), text=f'{v[1]} - {v[2]}', tags=v[0])

    def rclick_event(self, event=None):
        """Вызов вспомогательного меню для взаимодействия с шаблонами"""
        row = self.listbox.identify_row(event.y)
        self.listbox.selection_set(row)
        state = 'normal' if row else 'disabled'
        menu = tk.Menu(tearoff=0)
        menu.add_command(label='Использовать', state=state, command=self.init_sample)
        menu.add_separator()
        menu.add_command(label='Добавить', command=self.edit_sample('add', None))
        menu.add_command(label='Редактировать', state=state, command=self.edit_sample('edit', self.get_sample))
        menu.add_command(label='Удалить', state=state, command=self.del_sample)
        menu.add_separator()
        menu.add_command(label='Посмотреть', state=state, command=lambda: self.see_sample(event))
        menu.post(x=event.x_root, y=event.y_root)

    def edit_sample(self, mode, func):
        """Замыкание для вызова окна редактирования/добавления шаблона"""
        if func is None:
            func = lambda: (None, '#Таг', '#Демонстрационный шаблон', None)
        def closure():
            SampleEditWindow(master=self.master.master.master, mode=mode, sample_tpl=func(), update_func=self.update_listbox)
        return closure

    def see_sample(self, event):
        """Просмотр содержимого шаблона"""
        *_, text = self.get_sample()
        TipWindow(master=self, mouse_event=event, text=''.join(text))

    def get_sample(self) -> tuple:
        """Возвращает id, tag, name, sample (текст) шаблона по выбранному значению в листобоксе"""
        item = self.listbox.item(self.listbox.selection()[0])
        tag, name = item['text'].split(' - ', maxsplit=1)
        return item['tags'][0], tag, name, self._samples.get_sample(item['tags'][0])

    def del_sample(self):
        """Удаление шаблона из хранилища"""
        self._samples.del_sample(self.get_sample()[0])
        self.update_listbox()

    def init_sample(self, event=None):
        """Инициализация текстового шаблона"""
        id, tag, sample_name, text = self.get_sample()
        sample_title = f'{tag} - {sample_name}'
        if '?%' not in text:
            self.clipboard_clear()
            self.clipboard_append(text)
            tkmb.showinfo(parent=self, title=sample_title, message='Шаблон скопирован в буфер обмена')
        else:
            InitSampleWindow(master=self.master.master.master, text=text, sample_title=sample_title)


class SampleEditWindow(ChildWindow):
    """Окно редактирования/добавление текстового шаблона"""
    _samples = MailSamples()
    width = 440
    height = 385

    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode')
        self.s_id, *sample_tpl = kwargs.pop('sample_tpl')
        self.update_func = kwargs.pop('update_func')
        self.widget_lst = []
        super().__init__(*args, **kwargs)
        self.widget_lst[0].focus_set()
        self.insert_def_values(sample_tpl)

    def main(self, *args, **kwargs):
        self.title('Добавление шаблона' if self.mode == 'add' else 'Изменение шаблона')
        ttk.Label(master=self, text='Таг шаблона').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        tag_entry = ttk.Entry(master=self)
        tag_entry.pack(padx=2, pady=(2, 0), expand=1, fill='x')
        ttk.Label(master=self, text='Имя шаблона').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        name_entry = ttk.Entry(master=self, width=50)
        name_entry.pack(padx=2, pady=(2, 0), expand=1, fill='x')
        ttk.Label(master=self, text='Текст').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        frame = ttk.Frame(master=self)
        frame.pack(expand=1, fill='both')
        text = tk.Text(master=frame, width=52, height=15, wrap='word')
        text.pack(side='left', padx=2, pady=(2, 0))
        text.bind('<Button-3>', self.rclick_event)
        scroll = ttk.Scrollbar(master=frame, command=text.yview)
        text.config(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        MyButton(master=self, text='Сохранить', width=18, command=self.save).place(x=150, y=357)
        MyButton(master=self, text='Закрыть', command=self.destroy).pack(pady=2, padx=(0, 2), anchor='e')
        self.widget_lst.extend((tag_entry, name_entry, text))

    def insert_def_values(self, sample_tpl):
        self.widget_lst[0].insert(0, sample_tpl[0])
        self.widget_lst[1].insert(0, sample_tpl[1])
        text = sample_tpl[2]
        if not text:
            text = ['Текстовые шаблоны поддерживают переменные элементы. При инициализации шаблона программа даст ',
                    'подсказку, что подставить вместо этого элемента. Если значение не было внесено в соответствующее ',
                    'поле, то будет подставлена пустая строка, а переменный элемент будет удален. Для добавления ',
                    'переменного элемента выделите слово литералом ?% по образцу, указанному в примере. Для корректной',
                    ' работы шаблона следует выделять слово с двух сторон. Использовать такую комбинацию символов ',
                    'в других целях нельзя.\n########## Пример ##########\n?%Имя?%, здравствуйте.\nВас беспокоит ',
                    'ФотокнигиОптом, Киров.\nПо поводу заказа ?%Номер заказа?%.']
            text = ''.join(text)
        self.widget_lst[2].insert('1.0', text)

    def rclick_event(self, event=None):
        """Событие для выделения слово литералами в тексте шаблона"""
        try:
            word = self.widget_lst[-1].selection_get()
            menu = tk.Menu(tearoff=0)
            menu.add_command(label='Снять выделение' if word.startswith('?%') and word.endswith('?%') else 'Выделить',
                             command=lambda: self.update_lit_of_word(word))
            menu.post(event.x_root, event.y_root)
        except Exception as err:
            pass

    def update_lit_of_word(self, word: str):
        """Вспомогательная ф-я для выделения слова"""
        word = word[2:-2] if word.startswith('?%') else '?%' + word + '?%'
        self.widget_lst[-1].replace(tk.SEL_FIRST, tk.SEL_LAST, word)

    def save(self):
        """Сохранение шаблона в библиотеку"""
        sample_tpl = self.s_id, self.widget_lst[0].get(), self.widget_lst[1].get(), self.widget_lst[2].get("1.0", "end")[:-1]
        self._samples.save(*sample_tpl)
        self.destroy()
        self.update_func()
        tkmb.showinfo(parent=self.master, title='Сохранение шаблона', message=f'Шаблон <{sample_tpl[2]}> сохранен')


class InitSampleWindow(ChildWindow):
    """Вспомогательное окно для заполнения переменных в текстовом шаблоне"""
    width = 194

    def __init__(self, *args, **kwargs):
        self.text = kwargs.pop('text').split('?%')
        self.sample_title = kwargs.pop('sample_title')
        self.height = 20 + 30 + len(self.text[1::2]) * 44
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
        """Создание сэмпла и помещение его в буфер обмена"""
        for i in range(len(self.widget_lst)):
            self.text[i * 2 + 1] = self.widget_lst[i].get()
        text = ''.join(self.text)
        self.master.clipboard_clear()
        self.master.clipboard_append(text)
        self.destroy()
        tkmb.showinfo(parent=self.master, title=self.sample_title, message='Шаблон скопирован в буфер обмена')
