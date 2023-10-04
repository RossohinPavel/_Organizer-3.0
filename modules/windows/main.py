from modules.app_manager import *
import modules.windows.source as source
from modules.windows.frames import *


class MainWindow(AppManagerR, source.tk.Tk):
    """Основное окно приложения"""
    def __init__(self):
        super().__init__()
        self.set_main_graph_settings()
        self.show_mw_headers()
        self.show_processing_line()
        self.show_common_line()

    def set_main_graph_settings(self):
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 PRE ALPHA')
        width, height = 500, 410
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)

    @staticmethod
    def russian_hotkeys(event):
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def destroy(self) -> None:
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if self.app_m.txtvars.tasks_queue.get() > 0:
            if not source.tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()

    def show_mw_headers(self):
        TxtVars()   # инициализация объекта для хранения текстовых переменных.
        self.show_log_and_tracker_frame()
        self.show_queue_lbl()

    def show_separator(self):
        source.tk.Frame(master=self, bg='black', width=1, height=1).pack(fill='x')

    def show_log_and_tracker_frame(self):
        """Отрисовка статуса процесса выполнения лога"""
        self.show_separator()
        frame = source.tk.Frame(master=self, height=20)
        frame.pack(fill='both')
        source.ttk.Label(master=frame, text='Трекер заказов:').place(x=0, y=0)
        source.ttk.Label(master=frame, text='Трекер файлов:').place(x=250, y=0)
        orders_trk = source.tk.StringVar(master=self, value='Выключен')
        source.ttk.Label(master=frame, textvariable=orders_trk).place(x=90, y=0)
        files_trk = source.tk.StringVar(master=self, value='Выключен')
        source.ttk.Label(master=frame, textvariable=files_trk).place(x=340, y=0)
        self.app_m.TxtVars.orders_trk = orders_trk
        self.app_m.TxtVars.files_trk = files_trk

    def show_queue_lbl(self):
        """Отрисовка виджета статуса трекера файлов"""
        self.show_separator()
        frame = source.tk.Frame(master=self, height=20)
        frame.pack(fill='both')
        source.ttk.Label(master=frame, text='Задач в очереди:').place(x=250, y=0)
        tasks_queue = source.tk.IntVar(master=self, value=0)
        source.ttk.Label(master=frame, textvariable=tasks_queue).place(x=347, y=0)
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
        left_frame = source.tk.Frame(master=frame, relief='raised', border=1)
        left_frame.pack(side='left', fill='both', expand=True)
        line1 = source.tk.Frame(master=left_frame)
        source.MyButton(master=line1, text='Фотобумага', command=None, width=15).pack(side='left')
        source.MyButton(master=line1, text='Полиграфия', command=None, width=15).pack(side='right', padx=(5, 0))
        line1.pack(anchor='nw', padx=(6, 0), pady=(6, 5))
        line2 = source.tk.Frame(master=left_frame)
        source.MyButton(master=line2, text='Альбомы', command=None, width=15).pack(side='left')
        source.MyButton(master=line2, text='Журналы', command=None, width=15).pack(side='right', padx=(5, 0))
        line2.pack(anchor='nw', padx=(6, 0))
        line3 = source.tk.Frame(master=left_frame)
        source.MyButton(master=line3, text='Холсты', command=None, width=15).pack(side='left')
        self.__dict__['add_btn'] = source.MyButton(master=line3, text='Дополнительно', command=self.show_add_btn_menu, width=15)
        self.__dict__['add_btn'].pack(side='right', padx=(5, 0))
        line3.pack(anchor='nw', padx=(6, 0), pady=(5, 7))

    def show_add_btn_menu(self):
        add_menu = source.tk.Menu(tearoff=0)
        add_menu.add_command(label="Обновить БД", command=self.app_m.tr.ot.manual)
        add_menu.post(self.__dict__['add_btn'].winfo_rootx(), self.__dict__['add_btn'].winfo_rooty() + 25)

    @staticmethod
    def show_processing_frame(frame):
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        processing_frame = source.tk.Frame(master=frame, width=250, relief='raised', border=1)
        processing_frame.pack(side='right', fill='both')
        ProcessingFrame(processing_frame)

    def show_common_line(self):
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        self.show_label('Общее', bg='#adc6ed')
        self.show_separator()
        frame = source.tk.Frame(master=self)
        frame.pack(anchor='nw', expand=1, fill='both')
        self.show_information_buttons(frame)
        self.show_information_frame(frame)

    def show_information_buttons(self, frame):
        """Отрисовка кнопок получения различной информации о заказах"""
        l_frame = source.tk.Frame(master=frame, relief='raised', border=1)
        l_frame.pack(side='left', anchor='nw')
        btn1 = source.MyButton(master=l_frame, text='СтикГен', command=self.update_info_frame(StickGenFrame), width=18)
        btn1.pack(padx=56, pady=(5, 0))
        btn2 = source.MyButton(master=l_frame, text='Планировщик', command=self.update_info_frame(PlanerFrame), width=18)
        btn2.pack(pady=(5, 0))
        btn3 = source.MyButton(master=l_frame, text='Текстовые шаблоны', command=self.update_info_frame(MailSamplesFrame), width=18)
        btn3.pack(pady=(5, 0))
        for _ in range(3):
            source.tk.Frame(master=l_frame, height=26, width=20).pack(pady=(5, 0))
        btn4 = source.MyButton(master=l_frame, text='Управление', width=18, command=self.update_info_frame(ControlFrame))
        btn4.pack(pady=(5, 5))

    def show_information_frame(self, frame):
        """Отрисовка фрейма отображения информации о заказах"""
        frame = source.tk.Frame(master=frame, relief='raised', border=1)
        frame.contained_obj = None
        setattr(self, 'info_frame', frame)
        frame.pack(side='right', expand=1, fill='both')

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


class TxtVars(AppManagerW):
    _alias = 'txtvars'

    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value
