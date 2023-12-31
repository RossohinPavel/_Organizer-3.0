from .source import *
from . import frames


class MainWindow(ttk.Window):
    """Основное окно приложения"""

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.3.0 BETA', iconphoto='data/assets/ico.png')
        # Запускаем определение стилей и получения изображений после __init__
        style_init()
        for k, v in IMAGES.items():
            IMAGES[k] = ttk.PhotoImage(master=self, file=v) #type: ignore
        self.set_main_graph_settings()

        # Отрисовываем колонку меню
        menu_column = ttk.Frame(self, padding=5)
        menu_column.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.todo = frames.MenuLabel('todo', menu_column, frames.PlanerFrame)
        self.todo.pack(anchor=ttkc.N, pady=(0, 5))

        self.social = frames.MenuLabel('social', menu_column, frames.MailSamplesFrame)
        self.social.pack(anchor=ttkc.N, pady=(0, 5))

        self.info = frames.MenuLabel('info', menu_column, ttk.Frame)
        self.info.pack(anchor=ttkc.N, pady=(0, 5))

        self.tracker = frames.MenuLabel('tracker', menu_column, ttk.Frame)
        self.tracker.pack(anchor=ttkc.N, pady=(0, 5))

        self.file = frames.MenuLabel('file', menu_column, frames.FileFrame)
        self.file.pack(anchor=ttkc.N, pady=(0, 5))

        self.stg = frames.MenuLabel('settings', menu_column, frames.SettingsFrame)
        self.stg.pack(anchor=ttkc.S, expand=1)

        # Разделитель
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side=ttkc.LEFT, fill=ttkc.Y)

        # Запускаем 1 фрейм - Лист задач
        self.todo.click(None)

    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        width, height = 550, 400
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        self.update_idletasks()

    @staticmethod
    def russian_hotkeys(event: tkinter.Event) -> None:
        """Эвент для срабатывания Ctrl+V на русской раскладке"""
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    # def destroy(self) -> None:
    #     """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
    #     ttl = 'Очередь задач не пуста'
    #     msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
    #     if AppManager.pf.queue > 0:
    #         if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
    #             return
    #     super().destroy()

    
    # def draw_log_tracker_widgets(self, container: ttk.Frame) -> None:
    #     """Отрисовка статуса процесса выполнения лога"""
    #     # Обработка нажатия на CheckButton
    #     def init(): 
    #         res = var.get()
    #         AppManager.stg.autolog = AppManager.ot.auto = res
    #         if not res: orders_trk.set('Выключен')

    #     # Checkbutton виджет управления теркером
    #     var = ttk.IntVar(self, AppManager.stg.autolog)
    #     chbtn = ttk.Checkbutton(
    #         master=container, 
    #         text='Трекер: ', 
    #         style='success-round-toggle', 
    #         onvalue=1, 
    #         offvalue=0,
    #         variable=var,
    #         command=init
    #         )
    #     chbtn.pack(side=ttkc.LEFT, padx=(3, 0))

    #     # Лейбл отрисовки статуса логгера
    #     AppManager.ot_var = orders_trk = ttk.StringVar(master=container, value='Выключен')
    #     ttk.Label(master=container, textvariable=orders_trk).pack(side=ttkc.LEFT)

