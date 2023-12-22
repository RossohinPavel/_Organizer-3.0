from .source import *


from . import frames
# from . import windows


class MainWindow(ttk.Window):
    """Основное окно приложения"""

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.2.0 BETA', iconphoto='data/assets/ico.png')
        # Запускаем определение стилей и получения изображений после __init__
        style_init()
        for k, v in IMAGES.items():
            IMAGES[k] = ttk.PhotoImage(master=self, file=v) #type: ignore
        self.set_main_graph_settings()

        # Отрисовываем колонку меню
        menu_column = ttk.Frame(self)
        menu_column.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.todo = frames.MenuLabel('todo', menu_column, frames.PlanerFrame)
        self.todo.pack(anchor=ttkc.N, padx=5, pady=(5, 0))

        ttk.Frame(menu_column).pack(expand=1)       # Заполнитель

        self.stg = frames.MenuLabel('settings', menu_column, frames.ControlFrame)
        self.stg.pack(anchor=ttkc.S, padx=5, pady=(0, 5))

        # Разделитель
        separator = ttk.Separator(self, orient='vertical')
        separator.pack(side=ttkc.LEFT, fill=ttkc.Y)

    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        width, height = 550, 350
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

    # def draw_header_frames(self) -> None:
    #     """Отрисовка фрейма - заголовка окна"""
    #     container = ttk.Frame(master=self, padding=(5, 5, 5, 0))
    #     container.pack(fill=ttkc.X)
    #     self.draw_log_tracker_widgets(container)
    #     self.draw_theme_switcher(container)
    
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

    # def draw_theme_switcher(self, container: ttk.Frame) -> None:
    #     """Отрисовка свитчера тем"""
    #     def switch_theme():
    #         """Переключение темы по нажатию"""
    #         theme = theme_var.get()
    #         style.theme_use(theme)
    #         AppManager.stg.theme = theme
    #         style_init()

    #     # Объект Style
    #     style = ttk.Style()

    #     # Переменная для хранения названия темы
    #     theme_var = ttk.StringVar(self, value=AppManager.stg.theme)

    #     # Выподающее меню
    #     menu = ttk.Menu(container)
    #     for name in style.theme_names():
    #         menu.add_radiobutton(label=name, variable=theme_var, command=switch_theme)

    #     # Кнопка для меню
    #     btn = ttk.Menubutton(
    #         container, 
    #         text='Темы', 
    #         style='ts.Outline.TMenubutton', 
    #         menu=menu, 
    #         cursor='hand2'
    #         )
    #     btn.pack(side=ttkc.RIGHT)

    #     # Вызываем ф-ю для того, чтобы применилась сохраненная тема
    #     switch_theme()
    
    # def draw_processing_widgets(self) -> None:
    #     """Отображение виджетов файловой обработки"""
    #     master = ttk.Frame(self, padding=(0, 2, 0 , 0))
    #     master.pack(fill=ttkc.X)

    #     # Контейнер для кнопок
    #     btn_container = ttk.Labelframe(
    #         master, 
    #         text='Обработка', 
    #         padding=(5, 0, 5, 5)
    #         )
    #     btn_container.pack(side=ttkc.LEFT, padx=5)

    #     # Отрисовка кнопок
    #     self.draw_processing_buttons(btn_container)
    #     self.draw_add_btn_menu(btn_container)

    #     # Отрисовка фрейма статуса выполнения процессов
    #     pf = AppManager.pf = frames.ProcessingFrame(master)
    #     pf.pack(
    #         side=ttkc.LEFT, 
    #         padx=(0, 5),
    #         fill=ttkc.BOTH,
    #         expand=1
    #         )

    # def draw_processing_buttons(self, container: ttk.Labelframe) -> None:
    #     """Отрисовка фрейма кнопок запуска обработчика файлов"""
    #     btn1 = ttk.Button(
    #         container, 
    #         text='Разметка обложек', 
    #         command=lambda: print(self.winfo_geometry())
    #         # command=lambda: CoverMarkerWindow(self), 
    #         )
    #     btn1.pack(fill=ttkc.X)
        
    #     btn2 = ttk.Button(
    #         container, 
    #         text='Раскодировка', 
    #         command=lambda: PageDecoderWindow(master=self), 
    #         )
    #     btn2.pack(fill=ttkc.X, pady=5)

    #     self.bind('<F1>', lambda _: AppManager.pf.__enter__())
    #      # # self.bind('<F1>', lambda _: btn1.invoke())
    #     # # self.bind('<F2>', lambda _: btn2.invoke())
    #     self.bind('<F2>', lambda _: AppManager.pf.__exit__())

    # def draw_add_btn_menu(self, container: ttk.Labelframe) -> None:
    #     """Отрисовка кнопки Дополнительно и меню под ней"""
    #     menu = ttk.Menu(master=container)

    #     menu.add_command(label='Обновить БД', command=lambda: AppManager.ot.manual_init())
    #     menu.add_command(label='Направляющие')
    #     menu.add_command(label='Холсты')
    #     menu.add_command(label='Замена')
    #     menu.add_command(label='Восстановление')
    #     menu.add_command(label='Роддом', command=lambda: windows.Roddom(self))

    #     btn = ttk.Menubutton(
    #         master=container, 
    #         text='Дополнительно', 
    #         menu=menu
    #         )
    #     btn.pack(fill=ttkc.X)

    #     self.bind('<F3>', lambda _: btn.event_generate('<<Invoke>>'))       
    
    # def draw_common_notebook(self) -> None:
    #     """Отображение остальных фреймов для работы с заказами, клиентами и др"""
    #     tab = ttk.Notebook(master=self)
    #     tab.pack(
    #         padx=5, 
    #         pady=5,
    #         fill=ttkc.BOTH,
    #         expand=1
    #         )
    #     # Закладки
    #     tab.add(frames.InfoFrame(tab), text='Информация')
    #     tab.add(
    #         ttk.Label(tab, text='test', background='red'), 
    #         text='Планировщик', 
    #         padding=5
    #         )
    #     tab.add(frames.MailSamplesFrame(tab).container, text='Общение')
    #     tab.add(frames.ControlFrame(tab), text='Управление')    
