import modules.windows.source as source
from modules.windows.settings import SettingsWindow
from modules.windows.library import LibraryWindow


class MainWindow(source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()
        self.set_main_graph_settings()
        self.show_menus()
        self.modules = dict((self.show_difficult_lbl(), self.show_processing_lbl(), *self.show_file_and_queue_lbl()))
        self.show_processing_line()
        self.show_common_line()
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)

    @staticmethod
    def russian_hotkeys(event):
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 BETA')
        width, height = 530, 420
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)

    def show_menus(self):
        """Отрисовка и инициализация менюшек"""
        main_menu = source.tk.Menu()
        main_menu.add_command(label="Настройки", command=lambda: SettingsWindow(self))
        main_menu.add_command(label='Библиотека', command=lambda: LibraryWindow(self))
        main_menu.add_command(label='Информация', command=lambda: print('None'))
        self.config(menu=main_menu)

    def show_separator(self): source.tk.Frame(master=self, bg='black', width=1, height=1).pack(fill='x')

    def show_difficult_lbl(self) -> tuple:
        """Отрисовка индекса сложности"""
        self.show_separator()
        difficult = source.tk.StringVar(master=self, value='Индекс сложности')
        source.tk.Label(master=self, textvariable=difficult).pack(fill='x')
        return 'difficult', difficult

    def show_processing_lbl(self) -> tuple:
        """Отрисовка статуса процесса выполнения лога"""
        self.show_separator()
        status_var = source.tk.StringVar(master=self, value='Статус выполнения')
        source.tk.Label(master=self, textvariable=status_var).pack(fill='x')
        return 'status', status_var

    def show_file_and_queue_lbl(self) -> tuple:
        """Отрисовка виджета статуса трекера файлов"""
        self.show_separator()
        frame = source.tk.Frame(master=self, bg='black')
        frame.pack(fill='both')
        left_frame = source.tk.Frame(master=frame, height=20)
        left_frame.pack(side='left', fill='both', expand=True)
        righ_frame = source.tk.Frame(master=frame, height=20)
        righ_frame.pack(side='right', fill='both', expand=True)
        file_tracker = source.tk.StringVar(master=frame, value='Трекер файлов выключен')
        source.ttk.Label(master=left_frame, textvariable=file_tracker).place(x=0, y=0)
        queue = source.tk.StringVar(master=frame, value='Задач в очереди:')
        source.ttk.Label(master=righ_frame, textvariable=queue).place(x=0, y=0)
        return ('file_tracker', file_tracker,), ('queue', queue)

    def show_label(self, text, bg=None):
        """Конструктор для отрисовка заголовка"""
        frame = source.tk.Frame(self, bg=bg)
        frame.pack(fill='x')
        label = source.ttk.Label(master=frame, text=text, background=bg)
        label.pack()

    def show_processing_line(self):
        """Отображение фреймов для обработки файлов"""
        self.show_separator()
        self.show_label('Обработка Файлов', bg='dark salmon')
        self.show_separator()
        frame = source.tk.Frame(master=self)
        frame.pack(fill='both')
        self.show_processing_buttons(frame)
        self.show_processing_frame(frame)

    @staticmethod
    def show_processing_buttons(frame):
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        left_frame = source.tk.Frame(master=frame, width=265, relief='raised', border=1)
        left_frame.pack(side='left', fill='both', expand=True, ipady=4)
        btn = (('Фотобумага', None, 'Полиграфия', None),
               ('Альбомы', None, 'Журналы', None),
               ('Холсты', None, 'Дополнительно', None))
        for ln, lc, rn, rc in btn:
            line = source.tk.Frame(master=left_frame)
            line.pack(fill='both', expand=True, padx=10)
            source.MyButton(master=line, text=ln, command=lc, width=15).pack(side='left', pady=3)
            source.MyButton(master=line, text=rn, command=rc, width=15).pack(side='right')

    @staticmethod
    def show_processing_frame(frame):
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        processing_frame = source.tk.Frame(master=frame, width=265, relief='raised', border=1)
        processing_frame.pack(side='right', fill='both')

    def show_common_line(self):
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        self.show_label('Общее', bg='#adc6ed')
        self.show_separator()
        frame = source.tk.Frame(master=self)
        frame.pack(fill='both')
        self.show_information_buttons(frame)
        self.show_information_frame(frame)

    @staticmethod
    def show_information_buttons(frame):
        """Отрисовка кнопок получения различной информации о заказах"""
        l_frame = source.tk.Frame(master=frame, width=265, relief='raised', border=1)
        l_frame.pack(side='left', fill='both', expand=True, ipady=4)
        source.MyButton(master=l_frame, text='СтикГен', width=18).pack(pady=4)
        source.MyButton(master=l_frame, text='Планировщик', width=18).pack(pady=4)
        source.MyButton(master=l_frame, text='Текстовые шаблоны', width=18).pack(pady=4)

    @staticmethod
    def show_information_frame(frame):
        """Отрисовка фрейма отображения информации о заказах"""
        source.tk.Frame(master=frame, width=268, height=218, bg='yellow').pack(side='right')
