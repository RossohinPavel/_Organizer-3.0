from ...source import *
from ....data_base import MailSamples
from .init_sample_window import InitSampleWindow
from .sample_edit_window import SampleEditWindow


SAMPLES = MailSamples()


class SampleButton(ttk.Menubutton):
    """Кнопка, реализующий логику работы с текстовым шаблоном"""

    _c_init = 'Использовать'
    _c_change = 'Изменить'
    _c_del = 'Удалить'
    _c_view = 'Содержание'

    def __init__(self, root: Any, sample_frame: Any, sample_id: int, sample_name: str, /, **kwargs):
        super().__init__(
            root, 
            cursor='hand2', 
            text=sample_name, 
            style='ts.Outline.TMenubutton', 
            **kwargs
        )
        self._sample_frame = sample_frame
        self._menu = ttk.Menu(self)
        self.sample_id = sample_id
        self.bind('<ButtonPress-1>', self.init_sample)
        self.bind('<ButtonPress-3>', self.show_menu)

    def init_sample(self, event: tkinter.Event | None = None) -> None:
        """Инициализация текстового шаблона"""
        self._menu.destroy()
        self['menu'] = ''
        tag, sample_name, text = SAMPLES.get(self.sample_id)
        sample_title = f'{tag} - {sample_name}'
        if '?%' not in text:
            self.clipboard_clear()
            self.clipboard_append(text)
            tkmb.showinfo(title=sample_title, message='Шаблон скопирован в буфер обмена.')
        else:
            InitSampleWindow(sample_title, text)
    
    def show_menu(self, event: tkinter.Event | None = None) -> None:
        """Отрисовка меню"""
        self['menu'] = self._menu = ttk.Menu(self)
        self._menu.add_command(label=self._c_init, command=self.init_sample)
        self._menu.add_command(label=self._c_change, command=self.edit_sample)
        self._menu.add_command(label=self._c_del, command=self.del_sample)
        self._menu.add_command(label=self._c_view, command=self.see_sample)
        self.event_generate('<<Invoke>>')
    
    def edit_sample(self) -> None:
        """Замыкание для вызова окна редактирования/добавления шаблона"""
        self.wait_window(SampleEditWindow(self.sample_id))
        self._sample_frame.update_frame()
    
    def del_sample(self):
        """Удаление шаблона из хранилища"""
        SAMPLES.delete(self.sample_id)
        self._sample_frame.update_frame()

    def see_sample(self):
        """Просмотр содержимого шаблона"""
        _, name, data = SAMPLES.get(self.sample_id)
        tkmb.showinfo(parent=AppManager.mw, title=name, message=''.join(data))


class MailSamplesFrame(ScrolledFrame):
    """Фрейм для работы с текстовыми шаблонами"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, bootstyle='round', padding=5)
        self.update_frame()

    def update_frame(self) -> None:
        """Наделение листобокса именами текстовых шаблонов"""
        for i in self.winfo_children():
            i.destroy()
        current_tag = frame = None
        for sid, tag, name in SAMPLES.get_headers():
            if current_tag != tag:
                current_tag = tag
                frame = ttk.LabelFrame(self, text=tag)
                frame.pack(fill='x', padx=(0, 13))
            SampleButton(frame, self, sid, name).pack(fill='x', padx=5, pady=(0, 5))
        ttk.Button(
            master=self, 
            width=16,
            text='Добавить',
            command=self.add_sample, 
            style='minibtn.Outline.TButton'
        ).pack(pady=5)
    
    def add_sample(self) -> None:
        """Добавление семпла в общий список"""
        self.wait_window(SampleEditWindow())
        self.update_frame()
