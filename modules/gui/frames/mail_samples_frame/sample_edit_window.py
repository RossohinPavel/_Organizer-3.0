from ..._source import *
from typing import Sequence
from ....mail_samples import MailSamples


class SampleEditWindow(ChildWindow):
    """Окно редактирования/добавление текстового шаблона"""
    _samples = MailSamples()
    width = 440
    height = 385

    def __init__(self, *args, **kwargs) -> None:
        self.mode = kwargs.pop('mode')
        self.s_id, *sample_tpl = kwargs.pop('sample_tpl')
        self.update_func = kwargs.pop('update_func')
        self.widget_lst = []
        super().__init__(*args, **kwargs)
        self.widget_lst[0].focus_set()
        self.insert_def_values(sample_tpl)

    def main(self, *args, **kwargs) -> None:
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

    def insert_def_values(self, sample_tpl: Sequence[str]) -> None:
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

    def rclick_event(self, event: tk.Event) -> None:
        """Событие для выделения слово литералами в тексте шаблона"""
        try:
            word = self.widget_lst[-1].selection_get()
            menu = tk.Menu(tearoff=0)
            menu.add_command(label='Снять выделение' if word.startswith('?%') and word.endswith('?%') else 'Выделить',
                             command=lambda: self.update_lit_of_word(word))
            menu.post(event.x_root, event.y_root)
        except Exception as err:
            pass

    def update_lit_of_word(self, word: str) -> None:
        """Вспомогательная ф-я для выделения слова"""
        word = word[2:-2] if word.startswith('?%') else '?%' + word + '?%'
        self.widget_lst[-1].replace(tk.SEL_FIRST, tk.SEL_LAST, word)

    def save(self) -> None:
        """Сохранение шаблона в библиотеку"""
        sample_tpl = self.s_id, self.widget_lst[0].get(), self.widget_lst[1].get(), self.widget_lst[2].get("1.0", "end")[:-1]
        self._samples.save(*sample_tpl)
        self.destroy()
        self.update_func()
        tkmb.showinfo(parent=self.master, title='Сохранение шаблона', message=f'Шаблон <{sample_tpl[2]}> сохранен')
