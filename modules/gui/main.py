from ttkbootstrap import Bootstyle
from ._source import *
from . import frames
# from . import windows


class MainWindow(tb.Window):
    WIN_GEOMETRY = Geometry(527, 511)
    LIN_GEOMETRY = Geometry(547, 527)

    # Определяем тип ОС
    match AppManager.SYSTEM:
        case 'win': _geometry = WIN_GEOMETRY
        case 'lin' | _: _geometry = LIN_GEOMETRY

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.1.0 PRE ALPHA')
        # Используем инициализатор стилей после того, как отработал __init__
        style_init()
        # Отрисовываем остальные виджеты
        self.set_main_graph_settings()
        self.show_header_frames()
        self.show_processing_column()
        self.show_common_line()
    
    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        width, height = self._geometry
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        self.iconphoto(True, tkinter.PhotoImage(data=AppManager.stg.app_ico))
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
    #     if AppManager.txtvars.queue.get() > 0:
    #         if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
    #             return
    #     super().destroy()

    def show_header_frames(self) -> None:
        """Отрисовка фрейма - заголовка окна"""
        container = tb.Frame(master=self, padding=(5, 6, 5, 0))
        container.pack(fill='x')
        self.show_log_tracker_widgets(container)
        self.show_theme_switcher(container)
    
    def show_log_tracker_widgets(self, container: tb.Frame) -> None:
        """Отрисовка статуса процесса выполнения лога"""
        # Обработка нажатия на CheckButton
        def init(): AppManager.stg.autolog = var.get()

        var = tb.IntVar(self, AppManager.stg.autolog)
        chbtn = tb.Checkbutton(
            master=container, 
            text='Трекер заказов: ', 
            style='success-round-toggle', 
            onvalue=1, 
            offvalue=0,
            variable=var,
            command=init
            )
        chbtn.pack(side='left', padx=(3, 0))
        orders_trk = tb.StringVar(master=container, value='Выключен')
        tb.Label(master=container, textvariable=orders_trk).pack(side='left')
        AppManager.txtvars.ot = orders_trk

    def show_theme_switcher(self, container: tb.Frame) -> None:
        """Отрисовка свитчера тем"""
        def switch_theme():
            """Переключение темы по нажатию"""
            theme = theme_var.get()
            style.theme_use(theme)
            AppManager.stg.theme = theme
            style_init()

        style = tb.Style()
        theme_var = tb.StringVar(self, value=AppManager.stg.theme)
        menu = tb.Menu(container)
        for name in style.theme_names():
            menu.add_radiobutton(label=name, variable=theme_var, command=switch_theme)
        btn = tb.Menubutton(container, text='Темы', style='ts.Outline.TMenubutton', menu=menu, cursor='hand2')
        btn.pack(side='right')
        switch_theme()
    
    def show_processing_column(self) -> None:
        """Отображение заголовка и фреймов файловой обработки"""
        l_container = tb.Frame(master=self, padding=(5, 0, 5, 5))
        l_container.pack(side='left', fill='y')
        btn_container = tb.Labelframe(l_container, text='Обработка', padding=(5, 0, 5, 5))
        btn_container.pack(fill='x')
        self.show_processing_buttons(btn_container)
        self.show_add_btn_menu(btn_container)
        psg_container = tb.Labelframe(l_container, text='Задач в очереди: ', padding=(5, 0, 3, 3))
        psg_container.pack(side='right', fill='y')
        # queue = ctk.IntVar(master=frame, value=0)
        # AppManager.txtvars.queue = queue
        self.show_processing_frame(psg_container)

    def show_processing_buttons(self, container: tb.Labelframe) -> None:
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        btn1 = tb.Button(container, text='Разметка обложек', command=lambda: CoverMarkerWindow(self), width=16)
        btn1.pack(fill='x')
        # self.bind('<F1>', lambda _: btn1.invoke())
        self.bind('<F1>', lambda _: AppManager.pf.__enter__())
        btn2 = tb.Button(container, text='Раскодировка', command=lambda: PageDecoderWindow(master=self), width=16)
        btn2.pack(fill='x', pady=5)
        # self.bind('<F2>', lambda _: btn2.invoke())
        self.bind('<F2>', lambda _: AppManager.pf.__exit__())

    def show_add_btn_menu(self, container: tb.Labelframe) -> None:
        """Отрисовка меню под кнопкой Дополнительно"""
        def init(value) -> None:
            """Обработка выбора в меню"""
            match value:
                case 'Обновить БД': pass
                case 'Направляющие': pass
                case 'Разместить по каналам': AppManager.pf.__enter__()
                case 'Холсты': AppManager.pf.__exit__()
                case 'Замена': pass
                case 'Восстановление': pass
                case 'Роддом': pass
            variable.set('Дополнительно')
        
        def event(event=None) -> None:
            """Ф-я хоткея"""
            menu.event_generate('<ButtonPress-1>')
            menu.event_generate('<ButtonRelease-1>')

        variable = tb.StringVar(master=self)
        values = ['Обновить БД', 'Направляющие', 'Разместить по каналам', 'Холсты', 'Замена', 'Восстановление', 'Роддом']
        menu = tb.OptionMenu(container, variable, 'Дополнительно', *values, command=init)
        menu.pack(fill='x')
        self.bind('<F3>', event)
    
    def show_processing_frame(self, container: tb.Labelframe) -> None:
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        tb.Frame(container, width=160).pack()
        AppManager.pf = frames.ProcessingFrame(container)
    
    def show_common_line(self) -> None:
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        tab = tb.Notebook(master=self)
        tab.pack(padx=(0, 5), pady=(8, 5), side='right', anchor='n', fill='y')
        tab1 = tb.Frame(tab)
        tab2 = tb.Label(tab, text='test', background='red')

        tab.add(tab1, text='Информация')
        tab.add(tab2, text='Планировщик', padding=5)
        tab.add(frames.MailSamplesFrame(tab).container, text='Общение', padding=5)
        tab.add(frames.ControlFrame(tab), text='Управление')
