from ._source import *
from typing import Callable, Sequence, Type
from .._appmanager import AppManager
from .frames import *
from . import windows


class MainWindow(tk.Tk):
    def __init__(self) -> None:
        """Основное окно приложения"""
        super().__init__()
        self.set_main_graph_settings()
        self.show_log_tracker_frame()
        self.show_processing_line()
        self.show_common_line()

    def set_app_img(self, img_tuple: Sequence[tuple[str, bytes]]) -> None:
        """Устанавливаем изображения, который будут использоваться в программе. Первое значение будет установлено как
        иконка приложения - все последующие станут атрибутами MainWindow"""
        self.iconphoto(True, tk.PhotoImage(data=img_tuple[0][1]))
        for attr_name, byte in img_tuple[1:]:
            setattr(self, attr_name, tk.PhotoImage(data=byte))
        self.update_idletasks()

    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3_0 PRE ALPHA')
        width, height = 444, 414
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_hotkeys()
        self.update_idletasks()

    @staticmethod
    def russian_hotkeys(event: tk.Event) -> None:
        """Эвент для срабатывания Ctrl+V на русской раскладке"""
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def bind_hotkeys(self) -> None:
        """Бинд хоткеев основного меню приложения"""
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        self.bind('<F1>', lambda _: CoverMarkerWindow(self))
        self.bind('<F2>', lambda _: PageDecoderWindow(master=self))
        self.bind('<F3>', lambda _: self.show_add_btn_menu())
        self.bind('<F5>', lambda _: self.update_info_frame(StickGenFrame)())
        self.bind('<F6>', lambda _: self.update_info_frame(PlanerFrame)())
        self.bind('<F7>', lambda _: self.update_info_frame(MailSamplesFrame)())

    def destroy(self) -> None:
        """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if AppManager.pf.queue.get() > 0:
            if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()

    def show_log_tracker_frame(self) -> None:
        """Отрисовка статуса процесса выполнения лога"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        container = ttk.Frame(master=self)
        container.pack(fill='x')
        ttk.Label(master=container, text='Трекер заказов:').pack(anchor='nw', side='left')
        orders_trk = tk.StringVar(master=container, value='Выключен')
        ttk.Label(master=container, textvariable=orders_trk).pack(side='left')
        AppManager.orders_trk = orders_trk

    def show_processing_line(self) -> None:
        """Отображение заголовка и фреймов файловой обработки"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        frame_style = ttk.Style(self)
        frame_style.configure('pl.TFrame', background='dark salmon')
        header_container = ttk.Frame(master=self, style='pl.TFrame')
        header_container.pack(fill='x')
        ttk.Label(master=header_container, text='Обработка Файлов', background='dark salmon').pack()
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        widgets_container = ttk.Frame(master=self)          # Отрисовка контейнеров для кнопопк и фрейма обработки
        widgets_container.pack(fill='x')
        left = ttk.Frame(master=widgets_container)
        left.pack(side='left', fill='x')
        self.show_processing_buttons(left)
        ttk.Frame(master=widgets_container, relief='solid').pack(side='left', fill='y')
        right = ttk.Frame(master=widgets_container)
        right.pack(side='left', fill='both', expand=1)
        self.show_processing_frame(right)

    def show_processing_buttons(self, frame: ttk.Frame) -> None:
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        btn1 = MyButton(master=frame, text='Разметка обложек', command=lambda: CoverMarkerWindow(self), width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = MyButton(master=frame, text='Раскодировка', command=lambda: PageDecoderWindow(master=self), width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = MyButton(master=frame, text='Дополнительно', command=self.show_add_btn_menu, width=15)
        btn3.pack(padx=7, pady=5)
        self.__dict__['add_btn'] = btn3

    def show_add_btn_menu(self) -> None:
        """Отрисовка меню под кнопкой Дополнительно"""
        add_menu = tk.Menu(tearoff=0)
        add_menu.add_command(label="Обновить БД") # AppManager.tr.ot.manual
        add_menu.add_separator()
        add_menu.add_command(label='Направляющие')  # command=lambda: CoverGuideLinerWindow(master=self)
        add_menu.add_command(label='Разместить по каналам')     #command=lambda: PlacementByChannelsWindow(master=self)
        add_menu.add_separator()
        add_menu.add_command(label='Холсты')    # command=lambda: CanvasHandlerWindow(master=self)
        add_menu.add_separator()
        add_menu.add_command(label='Замена')    # command=lambda: ImageReplacementWindow(master=self)
        add_menu.add_command(label='Восстановление')
        add_menu.add_separator()
        add_menu.add_command(label='Роддом', command=lambda: windows.Roddom(master=self))
        add_menu.post(self.__dict__['add_btn'].winfo_rootx(), self.__dict__['add_btn'].winfo_rooty() + 25)

    @staticmethod
    def show_processing_frame(frame: ttk.Frame) -> None:
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        proc_frm = ProcessingFrame(master=frame, text='Заданий в очереди:')
        AppManager.pf = proc_frm
        proc_frm.pack(side='left', fill='both', expand=1)

    def show_common_line(self) -> None:
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        frame_style = ttk.Style(self)
        frame_style.configure('cl.TFrame', background='#adc6ed')
        header_container = ttk.Frame(master=self, style='cl.TFrame')
        header_container.pack(fill='x')
        ttk.Label(master=header_container, text='Общее', background='#adc6ed').pack()
        ttk.Frame(master=self, relief='solid').pack(fill='x')
        widgets_container = ttk.Frame(master=self)          # Отрисовка контейнеров для кнопопк и фрейма обработки
        widgets_container.pack(fill='x')
        left = ttk.Frame(master=widgets_container)
        left.pack(side='left', fill='x')
        ttk.Frame(master=widgets_container, relief='solid').pack(side='left', fill='y')
        right = ttk.Frame(master=widgets_container)
        right.pack(side='left', fill='both', expand=1)
        setattr(right, 'container', None)
        setattr(self, 'info_frame', right)  # Добавляем атрибут на self, чтобы работало замыкание переключения виджетов
        self.show_information_buttons(left)

    def show_information_buttons(self, frame: ttk.Frame) -> None:
        """Отрисовка кнопок получения различной информации о заказах"""
        btn1 = MyButton(master=frame, text='СтикГен', command=self.update_info_frame(StickGenFrame), width=15)
        btn1.pack(padx=7, pady=(5, 0))
        btn2 = MyButton(master=frame, text='Планировщик', command=self.update_info_frame(PlanerFrame), width=15)
        btn2.pack(padx=7, pady=(5, 0))
        btn3 = MyButton(master=frame, text='Шаблоны писем', command=self.update_info_frame(MailSamplesFrame), width=15)
        btn3.pack(padx=7, pady=(5, 0))
        for _ in range(4):
            tk.Frame(master=frame, height=26, width=20).pack(padx=7, pady=(5, 0))
        btn4 = MyButton(master=frame, text='Управление', width=15, command=self.update_info_frame(ControlFrame))
        btn4.pack(pady=(5, 5))
        ttk.Frame(master=frame, relief='solid').pack(side='left', fill='y')

    def update_info_frame(self, obj_link: Type[ttk.Frame]) -> Callable[[], None]:
        """Замыкание для реализации логики отрисовки информации на info_frame"""
        info_frame = getattr(self, 'info_frame')
        def closure() -> None:
            for frame in info_frame.winfo_children():
                frame.destroy()
            if info_frame.container == obj_link:
                info_frame.container = None
            else:
                info_frame.container = obj_link
                obj_link(info_frame).pack(fill='both', expand=1)
        return closure
