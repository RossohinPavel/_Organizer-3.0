from ttkbootstrap import widgets
from ._source import *
from appmanager import AppManager
from . import frames
# from . import windows


class MainWindow(tb.Window):
    win_geometry = Geometry('444x414', '478x475')

    def __init__(self) -> None:
        super().__init__()
        self.set_main_graph_settings()
        self.show_header_frames()
        self.show_processing_column()
        self.show_common_line()
    
    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3.1.0 PRE ALPHA')
        # self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        # self.resizable(False, False)
        # self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        # self.update_idletasks()

    # @staticmethod
    # def russian_hotkeys(event: tkinter.Event) -> None:
    #     """Эвент для срабатывания Ctrl+V на русской раскладке_assist/requirements.txt"""
    #     if event.keycode == 86 and event.keysym == '??':
    #         event.widget.event_generate('<<Paste>>')

    # def destroy(self) -> None:
    #     """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
    #     ttl = 'Очередь задач не пуста'
    #     msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
    #     if AppManager.txtvars.queue.get() > 0:
    #         if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
    #             return
    #     super().destroy()
    
    # def set_app_img(self, img_tuple: Sequence[tuple[str, bytes]]) -> None:
    #     """Устанавливаем изображения, который будут использоваться в программе. Первое значение будет установлено как
    #     иконка приложения - все последующие станут атрибутами MainWindow"""
    #     self.iconphoto(True, tkinter.PhotoImage(data=img_tuple[0][1]))
    #     for attr_name, byte in img_tuple[1:]:
    #         setattr(self, attr_name, tkinter.PhotoImage(data=byte))
    #     self.update_idletasks()

    def show_header_frames(self) -> None:
        container = tb.Frame(master=self, padding=(5, 5, 5, 0))
        container.pack(fill='x')
        self.show_log_tracker_widgets(container)
        self.show_theme_switcher(container)
    
    def show_log_tracker_widgets(self, container: tb.Frame):
        """Отрисовка статуса процесса выполнения лога"""
        tb.Checkbutton(master=container, text='Трекер заказов: ', style='success-round-toggle').pack(side='left', padx=(3, 0))
        # orders_trk = tb.StringVar(master=container, value='Выключен')
        tb.Label(master=container, text='Выключен').pack(side='left')
        # # AppManager.txtvars.ot = orders_trk

    def show_theme_switcher(self, container: tb.Frame):
        style = tb.Style()
        menu = tb.Menu(container)
        for name in style.theme_names():
            menu.add_radiobutton(label=name)
        btn = tb.Menubutton(container, text='Темы', style="info-outline", menu=menu)
        btn.pack(side='right')
    
    def show_processing_column(self) -> None:
        """Отображение заголовка и фреймов файловой обработки"""
        l_container = tb.Frame(master=self, padding=(5, 0, 5, 5))
        l_container.pack(side='left')
        btn_container = tb.Labelframe(l_container, text='Обработка')
        btn_container.pack()
        self.show_processing_buttons(btn_container)
        self.show_add_btn_menu(btn_container)
        psg_container = tb.Labelframe(l_container, text='Задач в очереди: ', padding=(5, 0, 5, 5))
        psg_container.pack(side='right')
        # queue = ctk.IntVar(master=frame, value=0)
        # AppManager.txtvars.queue = queue
        self.show_processing_frame(psg_container)

    def show_processing_buttons(self, container: tb.Labelframe) -> None:
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        btn1 = tb.Button(container, text='Разметка обложек', command=lambda: CoverMarkerWindow(self), width=16)
        btn1.pack(fill='x', pady=(5, 0))
        self.bind('<F1>', lambda _: btn1.invoke())
        btn2 = tb.Button(container, text='Раскодировка', command=lambda: PageDecoderWindow(master=self), width=16)
        btn2.pack(fill='x', pady=5)
        self.bind('<F2>', lambda _: btn2.invoke())

    def show_add_btn_menu(self, container: tb.Labelframe) -> None:
        """Отрисовка меню под кнопкой Дополнительно"""
        def init(value) -> None:
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
            menu.event_generate('<ButtonPress-1>')
            menu.event_generate('<ButtonRelease-1>')

        variable = tb.StringVar(master=self)
        values = ['Обновить БД', 'Направляющие', 'Разместить по каналам', 'Холсты', 'Замена', 'Восстановление', 'Роддом']
        menu = tb.OptionMenu(container, variable, 'Дополнительно', *values, command=init)
        menu.pack(fill='x')
        self.bind('<F3>', event)
    
    def show_processing_frame(self, container: tb.Labelframe) -> None:
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        tb.Label(master=container, text='Module').pack(anchor='w')
        tb.Meter(container, metersize=160, interactive=True, textfont='-size 18 -weight bold', subtext='long_file_name').pack()
        tb.Meter(container, metersize=160, interactive=True, textfont='-size 18 -weight bold', subtext='long_file_name').pack()
    #     AppManager.pf = frames.ProcessingFrame(frame=bar)
    
    def show_common_line(self) -> None:
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        tab = tb.Notebook(master=self)
        tab.pack(padx=5, pady=(0, 5), side='right', anchor='n')
        tab1 = tb.Frame(tab)
        tab2 = tb.Frame(tab)
        tab3 = tb.Frame(tab)

        lbl = tb.Label(tab1, text='test')
        lbl.pack()

        tab.add(tab1, text='СтикерГен')
        tab.add(tab2, text='Планировщик')
        tab.add(tab3, text='Шаблоны')
        tab.add(frames.ControlFrame(tab), text='Управление')
    #     container = tb.Frame(master=self, padding=5)          # Отрисовка контейнеров для кнопопк и фрейма обработки
    #     container.pack()
    #     left = tb.Labelframe(master=container, text='Общее')
    #     left.pack()
    #     right = tb.Frame(master=container)
    #     right.pack()
    #     # self.closure = self.closure(right)  #type: ignore
    #     self.show_information_buttons(left) # Кнопки отрисовываем в самом конце, чтобы работало замыкание
        
    # def closure(self, master: tb.Frame) -> Callable:
    #     """Замыкание для отрисовки общих виджетов"""
    #     container = None
    #     def inner_closure(func: Callable[[tb.Frame], None]) -> Callable[[], None]:
    #         def wrapper() -> None:
    #             for frame in master.winfo_children():
    #                 frame.destroy()
    #             nonlocal container
    #             if func == container:
    #                 container = None
    #             else:
    #                 container = func
    #                 func(master)
    #         return wrapper
    #     return inner_closure

    # def show_information_buttons(self, frame: tb.Frame) -> None:
    #     """Отрисовка кнопок получения различной информации о заказах"""
    #     btn1 = tb.Button(master=frame, text='СтикГен')
    #     btn1.pack(padx=5, pady=(5, 0), side='top')
    #     self.bind('<F5>', lambda _: btn1.invoke())
    #     btn2 = tb.Button(master=frame, text='Планировщик')
    #     btn2.pack(padx=5, pady=(5, 0), side='top')
    #     self.bind('<F6>', lambda _: btn2.invoke())
    #     btn3 = tb.Button(master=frame, text='Шаблоны писем')    #type: ignore
    #     btn3.pack(padx=5, pady=(5, 0), side='top')
    #     self.bind('<F7>', lambda _: btn3.invoke())
    #     btn4 = tb.Button(master=frame, text='Управление')    #type: ignore
    #     btn4.pack(padx=5, pady=(5, 5), side='bottom')
    #     self.bind('<F8>', lambda _: btn4.invoke())
