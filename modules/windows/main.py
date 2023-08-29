import modules.windows.source as source
from modules.windows.settings import SettingsWindow
from modules.windows.library import LibraryWindow


class MainWindow(source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self, settings: object, library: object, monitor: object):
        super().__init__()
        self.settings = settings
        self.library = library
        self.set_main_graph_settings()
        self.show_menus()
        self.monitor = monitor
        self.monitor.txt_vars = self.init_monitor_vars()
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
        width, height = 532, 420
        self.geometry(f'{width}x{height}+'
                      f'{(self.winfo_screenwidth() - width) // 2}+'
                      f'{(self.winfo_screenheight() - height) // 2}')
        self.resizable(False, False)

    def show_menus(self):
        """Отрисовка и инициализация менюшек"""
        main_menu = source.tk.Menu()
        main_menu.add_command(label="Настройки", command=lambda: SettingsWindow(self))
        main_menu.add_command(label='Библиотека', command=lambda: LibraryWindow(self))
        main_menu.add_command(label='Информация', command=lambda: print('None'))
        self.config(menu=main_menu)

    def init_monitor_vars(self, row=0) -> dict:
        """Инициализация текстовых переменных для монитора файлов и отрисовки соответсвующий виджетов"""
        monitor_vars = (self.show_orders_count_lbl(row), self.show_processing_lbl(row),
                        self.show_file_lbl(row), self.show_difficult_lbl(row))
        return dict(monitor_vars)

    def show_separator(self, height=1, width=1, row=0, column=0, rowspan=1, columnspan=1, sticky='SW'):
        """Отрисовка полоски разделителя между виджетами"""
        separator = source.tk.Frame(master=self, bg='black', width=width, height=height)
        separator.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

    def show_orders_count_lbl(self, row) -> tuple:
        """Отрисовка счетчика отслеживаемых заказов и счетчика времени до следующего сканирования"""
        frame = source.tk.Frame(self, borderwidth=1, relief='solid')
        frame.grid(row=row, column=0, rowspan=7, columnspan=3, sticky='NSEW')
        orders_count_var = source.tk.StringVar(master=self, value='5500')
        orders_count_lbl = source.ttk.Label(master=frame, textvariable=orders_count_var)
        orders_count_lbl.pack(side='top', expand=1)
        return 'orders_count', orders_count_var,

    def show_processing_lbl(self, row) -> tuple:
        """Отрисовка статуса процесса выполнения лога"""
        self.show_separator(row=row, column=3, columnspan=18, sticky='EW')
        status_var = source.tk.StringVar(master=self, value='Статус выполнения')
        status_lbl = source.ttk.Label(master=self, textvariable=status_var)
        status_lbl.grid(row=row+1, column=3, columnspan=18, sticky='EW')
        self.show_separator(row=row+2, column=3, columnspan=18, sticky='EW')
        return 'status', status_var

    def show_file_lbl(self, row) -> tuple:
        """Отрисовка информации о файлах, которые копируются в место для печати. Отображает нераспознанные тиражи"""
        file = source.tk.StringVar(master=self, value='Файлы для копирования')
        file_lbl = source.ttk.Label(master=self, textvariable=file)
        file_lbl.grid(row=row+3, column=3, columnspan=18, sticky='w')
        self.show_separator(row=row+4, column=3, columnspan=18, sticky='EW')
        return 'file', file

    def show_difficult_lbl(self, row) -> tuple:
        """Отрисовка индекса сложности"""
        difficult = source.tk.StringVar(master=self, value='Индекс сложности')
        difficult_lbl = source.ttk.Label(master=self, textvariable=difficult)
        difficult_lbl.grid(row=row+5, column=3, columnspan=18, sticky='w')
        self.show_separator(row=row+6, column=3, columnspan=18, sticky='EW')
        return 'difficult', difficult

    def show_label(self, text, bg=None, row=0):
        """Конструктор для отрисовка заголовка"""
        frame = source.tk.Frame(self, bg=bg)
        frame.grid(row=row, column=0, columnspan=21, sticky='EW')
        label = source.ttk.Label(master=frame, text=text, background=bg)
        label.pack()
        self.show_separator(row=row+1, column=0, columnspan=21, width=532)

    def show_processing_line(self, row=7):
        """Отображение фреймов для обработки файлов"""
        self.show_label('Обработка Файлов', bg='dark salmon', row=row)
        self.show_processing_buttons(row+2)
        self.show_processing_frame(row+2)

    def show_processing_buttons(self, row=0):
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        self.show_separator(row=row, column=10, rowspan=5, sticky='NSEW')
        fb_btn = source.MyButton(master=self, text='Фотобумага')
        fb_btn.grid(row=row+1, column=0, columnspan=5, sticky='ew', padx=3, pady=3)
        pb_btn = source.MyButton(master=self, text='Полиграфия')
        pb_btn.grid(row=row+1, column=5, columnspan=5, sticky='ew', padx=3, pady=3)
        alb_btn = source.MyButton(master=self, text='Альбомы')
        alb_btn.grid(row=row+2, column=0, columnspan=5, sticky='ew', padx=3, pady=3)
        jur_btn = source.MyButton(master=self, text='Журналы')
        jur_btn.grid(row=row+2, column=5, columnspan=5, sticky='ew', padx=3, pady=3)
        cnv_btn = source.MyButton(master=self, text='Холсты')
        cnv_btn.grid(row=row+3, column=0, columnspan=5, sticky='ew', padx=3, pady=3)
        add_btn = source.MyButton(master=self, text='Дополнительно')
        add_btn.grid(row=row+3, column=5, columnspan=5, sticky='ew', padx=3, pady=3)
        self.show_separator(row=row+4, column=0, columnspan=10, sticky='ew', width=268)

    def show_processing_frame(self, row):
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        processing_frame = source.tk.Frame(master=self, width=269, height=100, bg='pink')
        processing_frame.grid(row=row, column=11, columnspan=10, rowspan=4, sticky='NSEW')
        self.show_separator(row=row+4, column=11, columnspan=10, width=269)

    def show_common_line(self, row=14):
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        self.show_label('Общее', bg='#adc6ed', row=row)
        self.show_information_buttons(row+2)
        self.show_information_frame(row+2)

    def show_information_buttons(self, row):
        """Отрисовка кнопок получения различной информации о заказах"""
        self.show_separator(row=row, column=10, sticky='NS', rowspan=40)
        stick_gen_btn = source.MyButton(master=self, text='СтикГен', width=17, command=self.monitor.run)
        stick_gen_btn.grid(row=row+1, column=0, columnspan=10, pady=3, sticky='N')
        palnner_btn = source.MyButton(master=self, text='Планировщик', width=17)
        palnner_btn.grid(row=row+2, column=0, columnspan=10, sticky='N')
        mail_samples_btn = source.MyButton(master=self, text='Текстовые шаблоны', width=17)
        mail_samples_btn.grid(row=row+3, column=0, columnspan=10, pady=3, sticky='N')

    def show_information_frame(self, row):
        """Отрисовка фрейма отображения информации о заказах"""
        information_frame = source.tk.Frame(master=self, width=268, height=218, bg='yellow')
        information_frame.grid(row=row, column=11, rowspan=30, columnspan=10, sticky='NSEW')
