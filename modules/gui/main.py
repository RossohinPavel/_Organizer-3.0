from ._source import *
from typing import Callable, Type
from appmanager import AppManager
from . import frames
from . import windows


class MainWindow(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.set_main_graph_settings()
        self.show_log_tracker_frame()
        self.show_processing_line()
        # self.show_common_line()
    
    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        self.title('Органайзер 3.1.0 PRE ALPHA')
        match AppManager.SYSTEM:
            case 'win': width, height = 444, 414
            case 'lin': width, height = 492, 435
            case _: width, height = 444, 414
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        # self.bind_hotkeys()
        self.update_idletasks()

    def show_log_tracker_frame(self) -> None:
        """Отрисовка статуса процесса выполнения лога"""
        container = ctk.CTkFrame(master=self, fg_color='transparent')
        container.pack(fill='x')
        switcher = ctk.CTkSwitch(master=container, text='Трекер заказов: ')
        switcher.pack(side='left')
        # orders_trk = tk.StringVar(master=container, value='Выключен')
        ctk.CTkLabel(master=container, text='Выключен').pack(side='left')
        # AppManager.txtvars.ot = orders_trk
    
    def show_processing_line(self) -> None:
        """Отображение заголовка и фреймов файловой обработки"""
        container = ctk.CTkFrame(master=self, fg_color='transparent')
        container.pack(anchor='nw', fill='both')
        left = ctk.CTkFrame(master=container)
        left.pack(side='left', fill='y', expand=1)
        self.show_processing_buttons(left)
        self.show_add_btn_menu(left)
        right = ctk.CTkFrame(master=container, height=1)
        right.pack(side='left', fill='x', expand=1)
        self.show_processing_frame(right)

    def show_processing_buttons(self, frame: ctk.CTkFrame) -> None:
        """Отрисовка фрейма кнопок запуска обработчика файлов"""
        btn1 = ctk.CTkButton(master=frame, text='Разметка обложек', command=lambda: CoverMarkerWindow(self))
        btn1.pack(padx=5, pady=(16, 0), expand=1)
        btn2 = ctk.CTkButton(master=frame, text='Раскодировка', command=lambda: PageDecoderWindow(master=self))
        btn2.pack(padx=5, pady=(5, 5), expand=1)

    def show_add_btn_menu(self, frame: ctk.CTkFrame) -> None:
        """Отрисовка меню под кнопкой Дополнительно"""
        def init(value: str) -> None:
            match value:
                case 'Обновить БД': pass
                case 'Направляющие': pass
                case 'Разместить по каналам': AppManager.pf.__enter__()
                case 'Холсты': AppManager.pf.__exit__()
                case 'Замена': pass
                case 'Восстановление': pass
                case 'Роддом': pass
            variable.set('Дополнительно')
        
        values = ['Обновить БД', 'Направляющие', 'Разместить по каналам', 'Холсты', 'Замена', 'Восстановление', 'Роддом']
        variable = ctk.StringVar(master=self)
        menu = ctk.CTkOptionMenu(master=frame, variable=variable, values=values, command=init)
        menu.pack(padx=5, pady=(0, 16), expand=1)
        init('pass')
    
    @staticmethod
    def show_processing_frame(frame: ctk.CTkFrame) -> None:
        """Отрисовка фрейма отображения прогресса обработки файлов"""
        header = ctk.CTkFrame(master=frame)
        header.pack(expand=1, fill='x')
        queue = ctk.IntVar(master=frame, value=0)
        ctk.CTkLabel(master=header, text='Заданий в очереди: ').pack(padx=(5, 0), side='left')
        ctk.CTkLabel(master=header, textvariable=queue).pack(side='left')
        ctk.CTkLabel(master=header, text='', width=400).pack(side='left')
        bar = ctk.CTkFrame(master=frame, width=340, height=109, fg_color='transparent')
        bar.pack(fill='x')
        proc_frm = frames.ProcessingFrame(frame=bar)
        AppManager.pf = proc_frm
    
    def show_common_line(self) -> None:
        """Отображение остальных фреймов для работы с заказами, клиентами и др"""
        widgets_container = ctk.CTkFrame(master=self, fg_color='transparent', height=270)          # Отрисовка контейнеров для кнопопк и фрейма обработки
        widgets_container.pack(fill='x')
        left = ctk.CTkFrame(master=widgets_container, height=270)
        left.pack(side='left', fill='both')
        right = ctk.CTkFrame(master=widgets_container, width=340, height=270)
        right.pack(side='left', fill='both', expand=1)
        setattr(self, 'widget_container', right)
        self.show_information_buttons(left)
    
    def init_info_frame(self, func: Callable[[ctk.CTkFrame], None]) -> Callable[[], None]:
        return lambda: func(getattr(self, 'widget_container'))

    def show_information_buttons(self, frame: ctk.CTkFrame) -> None:
        """Отрисовка кнопок получения различной информации о заказах"""
        btn1 = ctk.CTkButton(master=frame, text='СтикГен', command=self.init_info_frame(ctk.CTkFrame))
        btn1.pack(padx=6, pady=(6, 0), side='top')
        btn2 = ctk.CTkButton(master=frame, text='Планировщик', command=self.init_info_frame(ctk.CTkFrame))
        btn2.pack(padx=6, pady=(6, 0), side='top')
        btn3 = ctk.CTkButton(master=frame, text='Шаблоны писем')
        btn3.pack(padx=6, pady=(6, 0), side='top')
        btn4 = ctk.CTkButton(master=frame, text='Управление', command=self.init_info_frame(frames.control_frame))
        btn4.pack(pady=(6, 6), side='bottom')
        btn5 = ctk.CTkButton(master=frame, text='STG', command=lambda: print(self.geometry()))
        btn5.pack(pady=(6, 6), side='bottom')
        

# class MainWindow(tk.Tk):
#     def __init__(self) -> None:
#         """Основное окно приложения"""
#         super().__init__()
#         

#     def set_app_img(self, img_tuple: Sequence[tuple[str, bytes]]) -> None:
#         """Устанавливаем изображения, который будут использоваться в программе. Первое значение будет установлено как
#         иконка приложения - все последующие станут атрибутами MainWindow"""
#         self.iconphoto(True, tk.PhotoImage(data=img_tuple[0][1]))
#         for attr_name, byte in img_tuple[1:]:
#             setattr(self, attr_name, tk.PhotoImage(data=byte))
#         self.update_idletasks()

#     def set_main_graph_settings(self) -> None:
#         """Основные настройки окна, положения и размера."""
#         self.title('Органайзер 3_0 PRE ALPHA')
#         width, height = 444, 414
#         self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
#         self.resizable(False, False)
#         self.bind_hotkeys()
#         self.update_idletasks()

#     @staticmethod
#     def russian_hotkeys(event: tk.Event) -> None:
#         """Эвент для срабатывания Ctrl+V на русской раскладке_assist/requirements.txt""
#         if event.keycode == 86 and event.keysym == '??':
#             event.widget.event_generate('<<Paste>>')

#     def bind_hotkeys(self) -> None:
#         """Бинд хоткеев основного меню приложения"""
#         self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
#         self.bind('<F1>', lambda _: CoverMarkerWindow(self))
#         self.bind('<F2>', lambda _: PageDecoderWindow(master=self))
#         self.bind('<F3>', lambda _: self.show_add_btn_menu())
#         self.bind('<F5>', lambda _: self.update_info_frame(StickGenFrame)())
#         self.bind('<F6>', lambda _: self.update_info_frame(PlanerFrame)())
#         self.bind('<F7>', lambda _: self.update_info_frame(MailSamplesFrame)())

#     def destroy(self) -> None:
#         """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
#         ttl = 'Очередь задач не пуста'
#         msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
#         if AppManager.txtvars.queue.get() > 0:
#             if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
#                 return
#         super().destroy()

