from ...source import *
from typing import NamedTuple
from ....data_base.mail_samples import MailSamples


SAMPLES = MailSamples()


class SampleWidgets(NamedTuple):
    sample_id: int | None
    tag: ttk.Combobox
    name: ttk.Entry
    text: ttk.Text


class SampleEditWindow(ChildWindow):
    """Окно редактирования/добавление текстового шаблона"""
    width = 394
    height = 441

    def __init__(self, sample_id: int | None = None) -> None:
        self._widgets : SampleWidgets
        super().__init__(
            AppManager.mw, 
            sample_id=sample_id, 
            title='Изменение шаблона' if sample_id else 'Добавление шаблона')
        self._widgets.tag.focus_set()

    def main(self, **kwargs) -> None:
        ttk.Label(master=self, text='Таг шаблона').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        tag = ttk.Combobox(self, cursor='xterm', values=tuple(x[1] for x in SAMPLES.get_headers()))
        tag.pack(padx=2, pady=(2, 0), expand=1, fill='x')
        ttk.Label(master=self, text='Имя шаблона').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        name = ttk.Entry(master=self, width=50)
        name.pack(padx=2, pady=(2, 0), expand=1, fill='x')
        ttk.Label(master=self, text='Текст').pack(padx=(3, 0), pady=(2, 0), anchor='nw')
        frame = ttk.Frame(master=self)
        frame.pack(expand=1, fill='both')
        text = ttk.Text(master=frame, width=52, height=15, wrap='word')
        text.pack(side='left', padx=2, pady=(2, 0), expand=1, fill='both')
        text.bind('<Control-space>', self.highlight_event)
        scroll = ttk.Scrollbar(master=frame, command=text.yview, style='round')
        text.config(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        ttk.Button(master=self, text='Сохранить', width=18, command=self.save).pack(pady=2, padx=(2, 0), side='left')
        ttk.Button(master=self, text='Отмена', width=18, command=self.destroy).pack(pady=2, padx=(0, 2), side='right')
        sample_id = kwargs['sample_id']
        self._widgets = SampleWidgets(sample_id, tag, name, text)
        self.insert_values(SAMPLES.get(sample_id) if sample_id else self.get_default_text())

    def insert_values(self, sample_tpl: tuple[str, str, str]) -> None:
        """Размещает полученную информацию по виджетам"""
        self._widgets.tag.insert('0', sample_tpl[0])
        self._widgets.name.insert('0', sample_tpl[1])
        self._widgets.text.insert('1.0',sample_tpl[2])

    def get_default_text(self) -> tuple[str, str, str]:
        """Получение информации по-умолчанию"""
        tag = 'Общие'
        name = 'Демонстрационный шаблон'
        text = (
            'Текстовые шаблоны (далее ТШ) служат для ускорения передачи информации. Но с большой силой ',
            'приходит и большая ответственность. Следует внимательно относиться к составлению, отправке и',
            ' удалению ТШ.\nДля добавления нового шаблона - вместо этой инструкции введите нужный текст. ',
            'Проверьте себя на грамматику, пунктуацию и, прежде всего, на простоту и полноту передаваемых смыслов.',
            '\nТШ поддерживают переменные элементы. При инициализации ТШ программа даст подсказку, что ',
            'подставить вместо переменного элемента. Если информация не была внесена в соответствующее ',
            'поле, то ничего подставлено не будет, а переменный элемент будет удален. Для добавления ',
            'переменного элемента выделите слово литералом ?% по образцу, указанному в примере. ',
            'Использовать такую комбинацию символов в других целях нельзя.\n',
            'Комбинация клавиш <Control-space> вставляет ?%?% в позицию курсора',
            '\n########## Пример ##########\n?%Имя?%, здравствуйте.\nВас беспокоит ',
            'ФотокнигиОптом, Киров.\nПо поводу заказа ?%Номер заказа?%.'
            )
        return tag, name, ''.join(text)

    def highlight_event(self, event: tkinter.Event) -> None:
        """Событие для выделения слово литералами в тексте шаблона"""
        self._widgets.text.insert('insert', '?%?%')

    def save(self) -> None:
        """Сохранение шаблона в библиотеку"""
        sid = self._widgets.sample_id
        tag = self._widgets.tag.get()
        name = self._widgets.name.get()
        text = self._widgets.text.get("1.0", "end")[:-1]
        if not name:
            tkmb.showwarning(parent=self, title='Предупреждение', message='Отсутствует имя шаблона')
            return
        # В зависимости от наличия тэга (существования шаблона) обновляем его или создаем новый
        if sid:   
            SAMPLES.update(sid, tag, name, text)
        else:
            SAMPLES.create(tag, name, text)
        self.destroy()
        tkmb.showinfo(parent=self.master, title='Сохранение шаблона', message=f'Шаблон <{name}> сохранен')
