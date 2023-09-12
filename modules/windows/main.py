import modules.windows.source as source
from modules.windows.settings import SettingsWindow
from modules.windows.library import LibraryWindow
from modules.app_manager import *


class MainWindow(AppManagerR, source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()
        self.set_main_graph_settings()
        self.show_menus()
        self.show_mw_headers()
        self.show_processing_line()
        self.show_common_line()

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 PRE ALPHA')
        width, height = 530, 420
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)

    @staticmethod
    def russian_hotkeys(event):
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def show_menus(self):
        """Отрисовка и инициализация менюшек"""
        main_menu = source.tk.Menu()
        main_menu.add_command(label="Настройки", command=lambda: SettingsWindow(self))
        main_menu.add_command(label='Библиотека', command=lambda: LibraryWindow(self))
        main_menu.add_command(label='Информация', command=lambda: print('None'))
        self.config(menu=main_menu)

    def show_mw_headers(self):
        TxtVars()   # инициализация объекта для хранения текстовых переменных.
        self.show_difficult_lbl()
        self.show_log_and_tracker_frame()
        self.show_queue_lbl()

    def show_separator(self):
        source.tk.Frame(master=self, bg='black', width=1, height=1).pack(fill='x')

    def show_difficult_lbl(self):
        """Отрисовка индекса сложности"""
        self.show_separator()
        var = source.tk.StringVar(master=self, value='Индекс сложности')
        self.app_m.TxtVars.difficult = var
        source.tk.Label(master=self, textvariable=var).pack(fill='x')

    def show_log_and_tracker_frame(self):
        """Отрисовка статуса процесса выполнения лога"""
        self.show_separator()
        frame = source.tk.Frame(master=self, height=20)
        frame.pack(fill='both')
        source.ttk.Label(master=frame, text='Трекер заказов:').place(x=0, y=0)
        source.ttk.Label(master=frame, text='Трекер файлов:').place(x=265, y=0)
        orders_trk = source.tk.StringVar(master=self, value='Выключен')
        source.ttk.Label(master=frame, textvariable=orders_trk).place(x=90, y=0)
        files_trk = source.tk.StringVar(master=self, value='Выключен')
        source.ttk.Label(master=frame, textvariable=files_trk).place(x=355, y=0)
        self.app_m.TxtVars.orders_trk = orders_trk
        self.app_m.TxtVars.files_trk = files_trk

    def show_queue_lbl(self):
        """Отрисовка виджета статуса трекера файлов"""
        self.show_separator()
        frame = source.tk.Frame(master=self, height=20)
        frame.pack(fill='both')
        source.ttk.Label(master=frame, text='Задач в очереди:').place(x=265, y=0)
        tasks_queue = source.tk.IntVar(master=self, value=0)
        source.ttk.Label(master=frame, textvariable=tasks_queue).place(x=361, y=0)
        self.app_m.TxtVars.tasks_queue = tasks_queue

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

    def show_processing_buttons(self, frame):
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        left_frame = source.tk.Frame(master=frame, width=265, relief='raised', border=1)
        left_frame.pack(side='left', fill='both', expand=True, ipady=4)
        for ln, lc, rn, rc in (('Фотобумага', None, 'Полиграфия', None), ('Альбомы', None, 'Журналы', None)):
            line = source.tk.Frame(master=left_frame)
            line.pack(fill='both', expand=True, padx=10)
            source.MyButton(master=line, text=ln, command=lc, width=15).pack(side='left', pady=3)
            source.MyButton(master=line, text=rn, command=rc, width=15).pack(side='right')
        line = source.tk.Frame(master=left_frame)
        line.pack(fill='both', expand=True, padx=10)
        source.MyButton(master=line, text='Холсты', command=None, width=15).pack(side='left', pady=3)
        self.__dict__['add_btn'] = source.MyButton(master=line, text='Дополнительно',
                                                   command=self.show_add_btn_list, width=15)
        self.__dict__['add_btn'].pack(side='right')

    def show_add_btn_list(self):
        add_menu = source.tk.Menu(tearoff=0)
        add_menu.add_command(label="Обновить БД", command=self.app_m.OrdersTracker.run)
        add_menu.post(self.__dict__['add_btn'].winfo_rootx(), self.__dict__['add_btn'].winfo_rooty())

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


class TxtVars(AppManagerW):
    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
