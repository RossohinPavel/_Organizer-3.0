from modules.app_manager import *
import modules.windows.source as source
from modules.windows.frames import *


class MainWindow(AppManagerR, source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()
        self.set_main_graph_settings()
        self.txt_vars = AppManagerW(group_name='txt_vars')   # Инициализация объекта для хранения текстовых переменных.
        self.show_log_tracker_frame()
        self.show_processing_line()
        self.show_common_line()

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 PRE ALPHA')
        width, height = 444, 414
        self.geometry(f'+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)

    @staticmethod
    def russian_hotkeys(event):
        """Эвент для срабатывания Ctrl+V на русской раскладке"""
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def destroy(self) -> None:
        """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if self.app_m.pf.queue.get() > 0:
            if not source.tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()

    def show_log_tracker_frame(self):
        """Отрисовка статуса процесса выполнения лога"""
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = source.ttk.Frame(master=self)
        container.pack(fill='x')
        source.ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        source.ttk.Label(master=container, text='Трекер заказов:').pack(anchor='nw', side='left')
        orders_trk = source.tk.StringVar(master=container, value='Выключен')
        source.ttk.Label(master=container, textvariable=orders_trk).pack(side='left')
        source.ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        self.txt_vars.orders_trk = orders_trk

    def show_processing_line(self):
        """Отображение фреймов для обработки файлов"""
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = source.ttk.Frame(master=self)
        container.pack(fill='x')
        source.ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        frame_style = source.ttk.Style(self)
        frame_style.configure('pl.TFrame', background='dark salmon')
        container_for_label = source.ttk.Frame(master=container, style='pl.TFrame')
        container_for_label.pack(side='left', fill='x', expand=1)
        source.ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        source.ttk.Label(master=container_for_label, text='Обработка Файлов', background='dark salmon').pack()
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        container_for_widgets = source.ttk.Frame(master=self)
        container_for_widgets.pack(fill='x')
        self.show_processing_buttons(container_for_widgets)
        self.show_processing_frame(container_for_widgets)

    def show_processing_buttons(self, frame):
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        source.ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        container = source.ttk.Frame(master=frame)
        container.pack(side='left', fill='x')
        btn1 = source.MyButton(master=container, text='Сетка на обложки', command=None, width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = source.MyButton(master=container, text='Раскодировка', command=None, width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = source.MyButton(master=container, text='Дополнительно', command=self.show_add_btn_menu, width=15)
        btn3.pack(padx=7, pady=5)
        self.__dict__['add_btn'] = btn3

    def show_add_btn_menu(self):
        """Отрисовка меню под кнопкой Дополнительно"""
        add_menu = source.tk.Menu(tearoff=0)
        add_menu.add_command(label="Обновить БД", command=self.app_m.tr.ot.manual)
        add_menu.add_separator()
        add_menu.add_command(label='Направляющие')
        add_menu.add_command(label='Разместить по каналам')
        add_menu.add_command(label='Холсты')
        add_menu.add_separator()
        add_menu.add_command(label='Роддом')
        add_menu.add_separator()
        add_menu.add_command(label='Бакап')
        add_menu.add_command(label='Замена')
        add_menu.add_command(label="Print Geometry", command=lambda: print(self.geometry()))
        add_menu.post(self.__dict__['add_btn'].winfo_rootx(), self.__dict__['add_btn'].winfo_rooty() + 25)

    @staticmethod
    def show_processing_frame(frame):
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        source.ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        proc_frm = ProcessingFrame(master=frame, text='Заданий в очереди:')
        proc_frm.pack(side='left', fill='both', expand=1)
        source.ttk.Frame(master=frame, relief='solid').pack(side='right', fill='y')

    def show_common_line(self):
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = source.ttk.Frame(master=self)
        container.pack(fill='x')
        source.ttk.Frame(master=container, relief='solid').pack(side='left', fill='y')
        frame_style = source.ttk.Style(self)
        frame_style.configure('cl.TFrame', background='#adc6ed')
        container_for_label = source.ttk.Frame(master=container, style='cl.TFrame')
        container_for_label.pack(side='left', fill='x', expand=1)
        source.ttk.Frame(master=container, relief='solid').pack(side='right', fill='y')
        source.ttk.Label(master=container_for_label, text='Общее', background='#adc6ed').pack()
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        container_for_widgets = source.ttk.Frame(master=self)
        container_for_widgets.pack(fill='x')
        source.ttk.Frame(master=self, relief='solid').pack(fill='x')
        self.show_information_buttons(container_for_widgets)
        self.show_information_frame(container_for_widgets)

    def show_information_buttons(self, frame):
        """Отрисовка кнопок получения различной информации о заказах"""
        source.ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')
        container = source.tk.Frame(master=frame)
        container.pack(side='left', fill='y')
        btn1 = source.MyButton(master=container, text='СтикГен', command=self.update_info_frame(StickGenFrame), width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = source.MyButton(master=container, text='Планировщик', command=self.update_info_frame(PlanerFrame), width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = source.MyButton(master=container, text='Шаблоны писем', command=self.update_info_frame(MailSamplesFrame), width=15)
        btn3.pack(padx=7, pady=(5, 0))
        for _ in range(4):
            source.tk.Frame(master=container, height=26, width=20).pack(padx=7, pady=(5, 0))
        btn4 = source.MyButton(master=container, text='Управление', width=15, command=self.update_info_frame(ControlFrame))
        btn4.pack(pady=(5, 5))
        source.ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')

    def show_information_frame(self, frame):
        """Отрисовка фрейма отображения информации о заказах"""
        frame = source.tk.Frame(master=frame)
        frame.contained_obj = None
        setattr(self, 'info_frame', frame)
        frame.pack(side='left', expand=1, fill='both')
        source.ttk.Frame(master=frame, relief='solid').pack(side='right', fill='y')

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
