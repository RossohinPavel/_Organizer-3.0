from gui._source import *
from ttkbootstrap.scrolled import ScrolledFrame
from mail_samples import MailSamples
# from .init_sample_window import InitSampleWindow
# from .sample_edit_window import SampleEditWindow


SAMPLES = MailSamples()


class SampleButton(tb.OptionMenu):
    _c_init = 'Использовать'
    _c_change = 'Изменить'
    _c_del = 'Удалить'
    _c_view = 'Содержание'

    def __init__(self, root: Any, sample_frame: Any, sample_id: int, sample_name: str, /, **kwargs):
        self.sample_frame = sample_frame
        self.sample_id = sample_id
        self.sample_name = sample_name
        self.var = tb.StringVar(root)
        super().__init__(root, 
                        self.var, 
                        *(sample_name, self._c_init, self._c_change, self._c_del, self._c_view),
                        **kwargs, style='mini.Outline.TMenubutton', 
                        command=self.init)
        self.bind('<ButtonPress-3>', lambda _: self.init_sample())

    def init(self, value: str | tb.StringVar) -> None:
        """Обработка нажатия в меню"""
        match value:
            case self._c_init: self.init_sample()
            case self._c_change: pass
            case self._c_del: self.del_sample()
            case self._c_view: self.see_sample()
        self.var.set(self.sample_name)
    
    def init_sample(self) -> None:
        """Инициализация текстового шаблона"""
        tag, sample_name, text = SAMPLES.get(self.sample_id)
        sample_title = f'{tag} - {sample_name}'
        if '?%' not in text:
            self.clipboard_clear()
            self.clipboard_append(text)
            Messagebox.show_info(parent=self, title=sample_title, message='Шаблон скопирован в буфер обмена')
        else:
            InitSampleWindow(master=self.master.master.master, text=text, sample_title=sample_title) #type: ignore
    
    def del_sample(self):
        """Удаление шаблона из хранилища"""
        SAMPLES.delete(self.sample_id)
        self.sample_frame.update_frame()

    def see_sample(self):
        """Просмотр содержимого шаблона"""
        _, name, data = SAMPLES.get(self.sample_id)
        Messagebox.show_info(parent=self.sample_frame.master, title=name, message=''.join(data))


class MailSamplesFrame(ScrolledFrame):
    """Фрейм для работы с текстовыми шаблонами"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, bootstyle='round', padding=0)
        self.update_frame()

    def update_frame(self) -> None:
        """Наделение листобокса именами текстовых шаблонов"""
        for i in self.winfo_children():
            i.destroy()
        current_tag = frame = None
        for sid, tag, name in SAMPLES.get_headers():
            if current_tag != tag:
                current_tag = tag
                frame = tb.LabelFrame(self, text=tag)
                frame.pack(fill='x', padx=(0, 18))
            SampleButton(frame, self, sid, name).pack(fill='x', padx=5, pady=(0, 5))

    # def edit_sample(self, mode: str, func: Callable[[], tuple] | None) -> Callable[[], None]:
    #     """Замыкание для вызова окна редактирования/добавления шаблона"""
    #     if func is None:
    #         func = lambda: (None, '#Таг', '#Демонстрационный шаблон', None) #type: ignore
    #     def closure() -> None:
    #         SampleEditWindow(master=self.master.master.master, mode=mode, sample_tpl=func(), update_func=self.update_listbox) #type: ignore
    #     return closure

