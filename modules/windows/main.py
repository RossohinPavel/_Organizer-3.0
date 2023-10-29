from ..app_manager import *
from .source import *
from .frames import *
from .handlers import *
from .roddom import RoddomWindow


class MainWindow(tk.Tk):
    """Основное окно приложения"""
    storage = AppManager.storage
    __new__ = AppManager.write_to_storage('mw')

    def __init__(self):
        super().__init__()
        self.set_main_graph_settings()
        self.txt_vars = AppManager.create_group('txt_vars')   # Инициализация объекта для хранения текстовых переменных.
        self.show_log_tracker_frame()
        self.show_processing_line()
        self.show_common_line()

    def set_app_img(self, img_tuple: tuple[str, bytes]):
        """Устанавливаем изображения, который будут использоваться в программе. Первое значение будет установлено как
        иконка приложения - все последующие станут атрибутами MainWindow"""
        self.iconphoto(True, tk.PhotoImage(data=img_tuple[0][1]))
        for attr_name, byte in img_tuple[1:]:
            setattr(self, attr_name, tk.PhotoImage(data=byte))

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 PRE ALPHA')
        width, height = 444, 414
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        self.update_idletasks()

    @staticmethod
    def russian_hotkeys(event):
        """Эвент для срабатывания Ctrl+V на русской раскладке"""
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def destroy(self) -> None:
        """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if self.storage.pf.queue.get() > 0:
            if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()

    def show_log_tracker_frame(self):
        """Отрисовка статуса процесса выполнения лога"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = ttk.Frame(master=self)
        container.pack(fill='x')
        ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        ttk.Label(master=container, text='Трекер заказов:').pack(anchor='nw', side='left')
        orders_trk = tk.StringVar(master=container, value='Выключен')
        ttk.Label(master=container, textvariable=orders_trk).pack(side='left')
        ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        self.txt_vars.orders_trk = orders_trk

    def show_processing_line(self):
        """Отображение фреймов для обработки файлов"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = ttk.Frame(master=self)
        container.pack(fill='x')
        ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        frame_style = ttk.Style(self)
        frame_style.configure('pl.TFrame', background='dark salmon')
        container_for_label = ttk.Frame(master=container, style='pl.TFrame')
        container_for_label.pack(side='left', fill='x', expand=1)
        ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        ttk.Label(master=container_for_label, text='Обработка Файлов', background='dark salmon').pack()
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container_for_widgets = ttk.Frame(master=self)
        container_for_widgets.pack(fill='x')
        self.show_processing_buttons(container_for_widgets)
        self.show_processing_frame(container_for_widgets)

    def show_processing_buttons(self, frame):
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        container = ttk.Frame(master=frame)
        container.pack(side='left', fill='x')
        btn1 = MyButton(master=container, text='Разметка обложек', command=lambda: CoverMarkerWindow(self), width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = MyButton(master=container, text='Раскодировка', command=lambda: PageDecoderWindow(master=self), width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = MyButton(master=container, text='Дополнительно', command=self.show_add_btn_menu, width=15)
        btn3.pack(padx=7, pady=5)
        self.__dict__['add_btn'] = btn3

    def show_add_btn_menu(self):
        """Отрисовка меню под кнопкой Дополнительно"""
        add_menu = tk.Menu(tearoff=0)
        add_menu.add_command(label="Обновить БД", command=self.storage.tr.ot.manual)
        add_menu.add_separator()
        add_menu.add_command(label='Направляющие', command=lambda: CoverGuideLinerWindow(master=self))
        add_menu.add_command(label='Разместить по каналам', command=lambda: PlacementByChannelsWindow(master=self))
        add_menu.add_separator()
        add_menu.add_command(label='Холсты', command=lambda: CanvasHandlerWindow(master=self))
        add_menu.add_separator()
        add_menu.add_command(label='Замена', command=lambda: ImageReplacementWindow(master=self))
        add_menu.add_command(label='Восстановление')
        add_menu.add_separator()
        add_menu.add_command(label='Роддом', command=lambda: RoddomWindow(master=self))
        add_menu.post(self.__dict__['add_btn'].winfo_rootx(), self.__dict__['add_btn'].winfo_rooty() + 25)

    @staticmethod
    def show_processing_frame(frame):
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        proc_frm = ProcessingFrame(master=frame, text='Заданий в очереди:')
        proc_frm.pack(side='left', fill='both', expand=1)
        ttk.Frame(master=frame, relief='solid').pack(side='right', fill='y')

    def show_common_line(self):
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = ttk.Frame(master=self)
        container.pack(fill='x')
        ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        frame_style = ttk.Style(self)
        frame_style.configure('cl.TFrame', background='#adc6ed')
        container_for_label = ttk.Frame(master=container, style='cl.TFrame')
        container_for_label.pack(side='left', fill='x', expand=1)
        ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        ttk.Label(master=container_for_label, text='Общее', background='#adc6ed').pack()
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container_for_widgets = ttk.Frame(master=self)
        container_for_widgets.pack(fill='x')
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        self.show_information_buttons(container_for_widgets)
        self.show_information_frame(container_for_widgets)

    def show_information_buttons(self, frame):
        """Отрисовка кнопок получения различной информации о заказах"""
        ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        container = tk.Frame(master=frame)
        container.pack(side='left', fill='y')
        btn1 = MyButton(master=container, text='СтикГен', command=self.update_info_frame(StickGenFrame), width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = MyButton(master=container, text='Планировщик', command=self.update_info_frame(PlanerFrame), width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = MyButton(master=container, text='Шаблоны писем', command=self.update_info_frame(MailSamplesFrame), width=15)
        btn3.pack(padx=7, pady=(5, 0))
        for _ in range(4):
            tk.Frame(master=container, height=26, width=20).pack(padx=7, pady=(5, 0))
        btn4 = MyButton(master=container, text='Управление', width=15, command=self.update_info_frame(ControlFrame))
        btn4.pack(pady=(5, 5))
        ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')

    def show_information_frame(self, frame):
        """Отрисовка фрейма отображения информации о заказах"""
        frame = tk.Frame(master=frame)
        frame.contained_obj = None
        setattr(self, 'info_frame', frame)
        frame.pack(side='left', expand=1, fill='both')
        ttk.Frame(master=frame, relief='solid').pack(side='right', fill='y')

    def update_info_frame(self, obj_link):
        """Замыкание для реализации логики отрисовки информации на info_frame"""
        def closure():
            info_frame = getattr(self, 'info_frame')
            for frame in info_frame.winfo_children():
                frame.destroy()
            if info_frame.contained_obj == obj_link:
                info_frame.contained_obj = None
            else:
                info_frame.contained_obj = obj_link
                obj_link(info_frame).pack(fill='both', expand=1)
        return closure
