from ..source import *
from .header_label import HeaderLabel

from ...descriptors import Z_disc
# from ..windows.library import LibraryWindow


class ControlFrame(ttk.Frame):
    """Фрейм основных настроек приложения"""

    def __init__(self, master: Any):
        super().__init__(master, padding=(5, 3, 5, 5))

        self.show_directory_widgets()
        # self.show_buttons()

    def show_log_check_depth_widgets(self) -> None:
        """Отрисовка виджетов для настройки глубины проверки лога"""
        def get_entry_value(event: tkinter.Event | None = None) -> None:
            """Получение информации из entry виджета и сохранение их в настроки"""
            value = entry_var.get()
            if value.isdigit():
                AppManager.stg.log_check_depth = int(value)
                update_label()
            entry.delete(0, ttkc.END)

        def update_label() -> None:
            """Обновление информации на лейбле"""
            value_lbl.configure(text=f'Глубина проверки лога: {AppManager.stg.log_check_depth} заказов (папок)')
        
        # Контейнер для виджетов
        log_frm = ttk.LabelFrame(
            self, 
            text='Трекер заказов',
            padding=(5, 0, 5 ,5)
            )
        log_frm.pack(fill=ttkc.BOTH)

        # Отрисовка лейбла для отображения информации
        value_lbl = ttk.Label(log_frm)
        value_lbl.pack(anchor=ttkc.NW, padx=5)
        update_label()

        # Энтри виджет
        entry_var = ttk.StringVar(master=log_frm)
        entry = ttk.Entry(log_frm, textvariable=entry_var)
        entry.pack(
            side=ttkc.LEFT, 
            padx=(0, 5), 
            fill=ttkc.X, 
            expand=1
            )
        entry.bind('<Return>', get_entry_value)

        # Кнопка для получения значений из энтри
        btn = ttk.Button(
            log_frm, 
            text='Задать', 
            command=get_entry_value
            )
        btn.pack(
            side=ttkc.RIGHT, 
            expand=1, 
            fill=ttkc.X, 
            )
    

    def show_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        z_disc = HeaderLabel(self, 'Диск загрузки заказов \'Z\'')
        z_disc.pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 3))

        def update_dir() -> None:
            """Получение информации из файлового диалога"""
            path = tkfd.askdirectory(
                parent=AppManager.mw, 
                initialdir=AppManager.stg.z_disc, 
                title=f'Выберите:'
                )

            if path:
                AppManager.stg.z_disc = path

        btn = ttk.Button(master=self, command=update_dir, style='l_jf.TButton')
        btn.pack(fill=ttkc.X)
        Z_disc.add_call(lambda e: btn.configure(text=e))
        # HeaderLabel(self, 'Диск операторов фотопечати \'Т\'')


        # dir_frm = ttk.LabelFrame(self, text='Рабочие директории')
        # dir_frm.pack(fill=ttkc.BOTH, pady=(5, 0))
        # self.show_directory_frame(dir_frm, 'Диск операторов фотопечати \'Т\'', 't_disc')
        # self.show_directory_frame(dir_frm, 'Диск загрузки заказов \'Z\'', 'z_disc')
        # self.show_directory_frame(dir_frm, 'Диск печати заказов \'О\'', 'o_disc')


    def show_directory_frame(self, master: ttk.LabelFrame, text: str, stg_attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        def update_dir() -> None:
            """Получение информации из файлового диалога"""
            path = tkfd.askdirectory(
                parent=AppManager.mw, 
                initialdir=getattr(AppManager.stg, stg_attr), 
                title=f'Выберите: {text}'
                )

            if path:
                setattr(AppManager.stg, stg_attr, path)
                btn.configure(text=path)
        
        # Лейбл с названием директории
        ttk.Label(master, text=text).pack(anchor='nw', padx=5)

        btn = ttk.Button(
            master=master,
            # text=getattr(AppManager.stg, stg_attr), 
            command=update_dir, 
            style='l_jf.TButton'
            )
        btn.pack(
            fill='x', 
            padx=5, 
            pady=(0, 5)
            )

    def show_buttons(self):
        """Отрисовка кнопок управления"""
        lib_btn = ttk.Button(
            master=self, 
            text='Библиотека', 
            width=13, 
            command=lambda: LibraryWindow()
            )
        lib_btn.pack(expand=1, anchor='s')
