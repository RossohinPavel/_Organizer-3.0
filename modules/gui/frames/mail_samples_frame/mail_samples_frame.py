from ..._source import *
from typing import Callable
from ....mail_samples import MailSamples
from .init_sample_window import InitSampleWindow
from .sample_edit_window import SampleEditWindow


class MailSamplesFrame(LabeledFrame):
    """Фрейм для работы с текстовыми шаблонами"""
    _samples = MailSamples()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, text='Текстовые шаблоны', **kwargs)
        self.listbox = ttk.Treeview(master=self.container, show='tree')
        self.show_main_widget()
        self.update_listbox()

    def show_main_widget(self) -> None:
        """Отрисовка основных виджетов"""
        self.listbox.pack(expand=1, fill='both', side='left')
        scroll = ttk.Scrollbar(master=self.container, command=self.listbox.yview)
        scroll.pack(side='right', fill='y')
        self.listbox.config(yscroll=scroll.set) # type: ignore
        self.listbox.bind('<Double-Button-1>', self.init_sample)
        self.listbox.bind('<Return>', self.init_sample)
        self.listbox.bind('<Button-3>', self.rclick_event)

    def update_listbox(self) -> None:
        """Наделение листобокса именами текстовых шаблонов"""
        for i in self.listbox.get_children(''):
            self.listbox.delete(i)
        for i, v in enumerate(self._samples.get_headers()):
            self.listbox.insert('', 'end', id=str(i), text=f'{v[1]} - {v[2]}', tags=v[0])

    def rclick_event(self, event: tk.Event) -> None:
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

    def edit_sample(self, mode: str, func: Callable | None) -> Callable[[], None]:
        """Замыкание для вызова окна редактирования/добавления шаблона"""
        if func is None:
            func = lambda: (None, '#Таг', '#Демонстрационный шаблон', None) #type: ignore
        def closure() -> None:
            SampleEditWindow(master=self.master.master.master, mode=mode, sample_tpl=func(), update_func=self.update_listbox) #type: ignore
        return closure

    def see_sample(self, event: tk.Event):
        """Просмотр содержимого шаблона"""
        *_, text = self.get_sample()
        TipWindow(master=self, mouse_event=event, text=''.join(text))

    def get_sample(self) -> tuple[int, str, str, str]:
        """Возвращает id, tag, name, sample (текст) шаблона по выбранному значению в листобоксе"""
        item = self.listbox.item(self.listbox.selection()[0])
        tag, name = item['text'].split(' - ', maxsplit=1)
        return item['tags'][0], tag, name, self._samples.get_sample(item['tags'][0]) #type: ignore

    def del_sample(self):
        """Удаление шаблона из хранилища"""
        self._samples.del_sample(self.get_sample()[0])
        self.update_listbox()

    def init_sample(self, event: tk.Event | None = None):
        """Инициализация текстового шаблона"""
        id, tag, sample_name, text = self.get_sample()
        sample_title = f'{tag} - {sample_name}'
        if '?%' not in text:
            self.clipboard_clear()
            self.clipboard_append(text)
            tkmb.showinfo(parent=self, title=sample_title, message='Шаблон скопирован в буфер обмена')
        else:
            InitSampleWindow(master=self.master.master.master, text=text, sample_title=sample_title) #type: ignore
