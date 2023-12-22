from ..source import *
from .header_label import HeaderLabel
from ...descriptors import Z_disc, O_disc, T_disc

# from ..windows.library import LibraryWindow


class ControlFrame(ttk.Frame):
    """Фрейм основных настроек приложения"""

    def __init__(self, master: Any):
        super().__init__(master, padding=5)
        self.show_directory_widgets()

    def show_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.show_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc')
        self.show_directory_frame('Диск печати заказов \'О\'', 'o_disc')
        self.show_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc')

    def _update_dir(self, attr: str) -> None:
        """Получение информации из файлового диалога"""
        path = tkfd.askdirectory(
            parent=AppManager.mw, 
            initialdir=getattr(AppManager.stg, attr), 
            title=f'Выберите расположение'
        )
        if path:
            setattr(AppManager.stg, attr, path)

    def show_directory_frame(self, text: str, attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        HeaderLabel(self, text).pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))
        btn = ttk.Button(
            self, 
            style='l_jf.Outline.TButton',
            command=lambda: self._update_dir(attr)
        )
        btn.pack(
            fill=ttkc.X, 
            pady=(0, 15), 
            padx=5
        )
        add_call_func = eval(f'{attr.capitalize()}.add_call')
        add_call_func(lambda e: btn.configure(text=e))


    # def show_buttons(self):
        # """Отрисовка кнопок управления"""
        # lib_btn = ttk.Button(
        #     master=self, 
        #     text='Библиотека', 
        #     width=13, 
        #     command=lambda: LibraryWindow()
        #     )
        # lib_btn.pack(expand=1, anchor='s')


    # def show_log_check_depth_widgets(self) -> None:
    #     """Отрисовка виджетов для настройки глубины проверки лога"""
    #     def get_entry_value(event: tkinter.Event | None = None) -> None:
    #         """Получение информации из entry виджета и сохранение их в настроки"""
    #         value = entry_var.get()
    #         if value.isdigit():
    #             AppManager.stg.log_check_depth = int(value)
    #             update_label()
    #         entry.delete(0, ttkc.END)

    #     def update_label() -> None:
    #         """Обновление информации на лейбле"""
    #         value_lbl.configure(text=f'Глубина проверки лога: {AppManager.stg.log_check_depth} заказов (папок)')
        
    #     # Контейнер для виджетов
    #     log_frm = ttk.LabelFrame(
    #         self, 
    #         text='Трекер заказов',
    #         padding=(5, 0, 5 ,5)
    #         )
    #     log_frm.pack(fill=ttkc.BOTH)

    #     # Отрисовка лейбла для отображения информации
    #     value_lbl = ttk.Label(log_frm)
    #     value_lbl.pack(anchor=ttkc.NW, padx=5)
    #     update_label()

    #     # Энтри виджет
    #     entry_var = ttk.StringVar(master=log_frm)
    #     entry = ttk.Entry(log_frm, textvariable=entry_var)
    #     entry.pack(
    #         side=ttkc.LEFT, 
    #         padx=(0, 5), 
    #         fill=ttkc.X, 
    #         expand=1
    #         )
    #     entry.bind('<Return>', get_entry_value)

    #     # Кнопка для получения значений из энтри
    #     btn = ttk.Button(
    #         log_frm, 
    #         text='Задать', 
    #         command=get_entry_value
    #         )
    #     btn.pack(
    #         side=ttkc.RIGHT, 
    #         expand=1, 
    #         fill=ttkc.X, 
    #         )
