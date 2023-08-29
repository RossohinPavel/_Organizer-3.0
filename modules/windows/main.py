import modules.windows.source as source
from modules.windows.settings import SettingsWindow
from modules.windows.library import LibraryWindow


class MainWindow(source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self, settings: object, library: object):
        super().__init__()
        self.settings = settings
        self.library = library
        self.set_main_graph_settings()
        self.show_menus()
        self.monitor_vars = self.init_monitor_vars()
        # self.show_processing_line()
        # self.show_other_line()
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)

    @staticmethod
    def russian_hotkeys(event):
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 BETA')
        width, height = 532, 450
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

    def init_monitor_vars(self) -> dict:
        """Инициализация текстовых переменных для монитора файлов и отрисовки соответсвующий виджетов"""
        frame = source.tk.Frame(self)
        monitor_vars = (self.show_orders_count_lbl(frame), self.show_time_lbl(frame), self.show_undetected_lbl(frame),
                        self.show_file_lbl(frame), self.show_difficult_lbl(frame))
        frame.pack(anchor='nw', expand=1, fill='both')
        return dict(monitor_vars)

    @staticmethod
    def show_separator(frame, height=1, width=1, row=0, column=0, rowspan=1, columnspan=1, sticky='SW'):
        """Отрисовка полоски разделителя между виджетами"""
        separator = source.tk.Frame(master=frame, bg='black', width=width, height=height)
        separator.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)

    def show_orders_count_lbl(self, frame) -> tuple:
        """Отрисовка счетчика отслеживаемых заказов"""
        self.show_separator(frame, row=0, column=0, rowspan=8, sticky='NS')
        self.show_separator(frame, row=0, column=1, width=80, sticky='EW')
        orders_count_var = source.tk.StringVar(master=frame, value='5500')
        orders_count_lbl = source.ttk.Label(master=frame, textvariable=orders_count_var)
        orders_count_lbl.grid(row=1, column=1, rowspan=6)
        self.show_separator(frame, row=0, column=2, rowspan=8, sticky='NS')
        self.show_separator(frame, row=7, column=1, sticky='EW')
        return 'orders_count', orders_count_var

    def show_time_lbl(self, frame) -> tuple:
        """Отрисовка счетчика времени до следующего сканирования"""
        self.show_separator(frame, row=0, column=3, width=50)
        time_var = source.tk.StringVar(master=frame, value='Время')
        time_lbl = source.ttk.Label(master=frame, textvariable=time_var)
        time_lbl.grid(row=1, column=3)
        self.show_separator(frame, row=2, column=3, sticky='EW')
        return 'time', time_var

    def show_undetected_lbl(self, frame) -> tuple:
        """Отрисовка списка нераспознанных тиражей"""
        self.show_separator(frame, row=0, column=4, width=399)
        self.show_separator(frame, row=0, column=5, rowspan=8, sticky='NS')
        undetected = source.tk.StringVar(master=frame, value='Нераспознанные тиражи')
        undetected_lbl = source.ttk.Label(master=frame, textvariable=undetected)
        undetected_lbl.grid(row=1, column=4, sticky='EW')
        self.show_separator(frame, row=2, column=4, sticky='EW')
        return 'undetected', undetected

    def show_file_lbl(self, frame) -> tuple:
        """Отрисовка информации о файлах, которые копируются в место для печати"""
        file = source.tk.StringVar(master=frame, value='Файлы для копирования')
        file_lbl = source.ttk.Label(master=frame, textvariable=file)
        file_lbl.grid(row=4, column=3, columnspan=2, sticky='w')
        self.show_separator(frame, row=5, column=3, columnspan=2, sticky='EW')
        return 'file', file

    def show_difficult_lbl(self, frame) -> tuple:
        """Отрисовка индекса сложности"""
        difficult = source.tk.StringVar(master=frame, value='Индекс сложности')
        difficult_lbl = source.ttk.Label(master=frame, textvariable=difficult)
        difficult_lbl.grid(row=6, column=3, columnspan=2, sticky='w')
        self.show_separator(frame, row=7, column=3, columnspan=2, sticky='EW')
        return 'difficult', difficult

    # def show_processing_buttons(self):
    #     """Отрисовка фрейма кнопок запуска обработчика файлов"""
    #     button_frame = source.tk.Frame(master=self, width=269)
    #     fb_and_pb_btn = source.CellTwoButton(master=button_frame, bt_l_name='Фотобумага', bt_r_name='Полиграфия')
    #     fb_and_pb_btn.pack()
    #     alb_and_jur_btn = source.CellTwoButton(master=button_frame, bt_l_name='Альбомы', bt_r_name='Журналы')
    #     alb_and_jur_btn.pack()
    #     canv_and_add_btn = source.CellTwoButton(master=button_frame, bt_l_name='Холсты', bt_r_name='Дополнительно')
    #     canv_and_add_btn.pack()
    #     button_frame.grid(row=8, column=0, columnspan=6, sticky='NSEW', pady=16)
    #     self.show_separator(row=8, column=6, sticky='NS')
    #     self.show_separator(row=9, column=0, columnspan=7, sticky='EW')
    #
    # def show_processing_frame(self):
    #     """Отрисовка фрейма отображения прогресса обработки файлов"""
    #     processing_frame = source.tk.Frame(master=self, width=269, height=10, bg='pink')
    #     processing_frame.grid(row=8, column=7, columnspan=5, sticky='NSEW')
    #     self.show_separator(row=9, column=7, columnspan=6, sticky='EW')
    #
    # def show_information_buttons(self):
    #     """Отрисовка кнопок получения различной информации о заказах"""
    #     button_frame = source.tk.Frame(master=self, width=269, height=128)
    #     stick_gen_btn = source.CellOneButton(master=button_frame, func_name='СтикГен')
    #     stick_gen_btn.pack()
    #     palnner_btn = source.CellOneButton(master=button_frame, func_name='Планировщик')
    #     palnner_btn.pack()
    #     mail_samples_btn = source.CellOneButton(master=button_frame, func_name='Текстовые шаблоны')
    #     mail_samples_btn.pack()
    #     button_frame.grid(row=12, column=0, columnspan=6, sticky='NSEW')
    #     self.show_separator(row=12, column=6, sticky='NS')
    #
    # def show_information_frame(self):
    #     """Отрисовка фрейма отображения информации о заказах"""
    #     information_frame = source.tk.Frame(master=self, width=269, height=220, bg='yellow')
    #     information_frame.grid(row=12, column=7, columnspan=5, sticky='NSEW')
    #
    #
    #
    # def show_label(self, master, text, bg=None, row=0, column=0, columnspan=12):
    #     """Отрисовка заголовка"""
    #     frame = source.tk.Frame(master=master, bg=bg)
    #     label = source.ttk.Label(master=frame, text=text, background=bg)
    #     label.pack()
    #     frame.grid(row=row, column=column, columnspan=columnspan, sticky='EW')
    #     self.show_separator(row=row+1, column=0, columnspan=12, sticky='EW')
    #
    #
    #
    # def show_processing_line(self):
    #     """Отображение фреймов для обработки файлов"""
    #     self.show_label(self, 'Обработка Файлов', row=6, bg='dark salmon')
    #     self.show_processing_buttons()
    #     self.show_processing_frame()
    #
    # def show_other_line(self):
    #     """Отображение остальных фреймов для работы с заказами, клиентами и др"""
    #     self.show_label(self, 'Общее', row=10, bg='#adc6ed')
    #     self.show_information_buttons()
    #     self.show_information_frame()
    #