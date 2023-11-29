from .._source import *
from ..windows.library import LibraryWindow


class ControlFrame(tb.Frame):
    """Фрейм основных настроек приложения"""

    def __init__(self, master: Any):
        super().__init__(master)
        self.show_log_check_depth_widgets()
        self.show_directory_widgets()
        self.show_buttons()


    def show_log_check_depth_widgets(self) -> None:
        """Отрисовка виджетов для настройки глубины проверки лога"""
        msg = ('Рекомендуемая глубина ~ 100 заказов.', 'Ограничено свободным объемом ОЗУ.')

        def get_entry_value(event: tkinter.Event | None = None) -> None:
            """Получение информации из entry виджета и сохранение их в настроки"""
            value = entry_var.get()
            if value.isdigit():
                AppManager.stg.log_check_depth = int(value)
                update_label()
            entry.delete(0, 'end')

        def update_label() -> None:
            """Обновление информации на лейбле"""
            value_lbl.configure(text=f'Текущее значение: {AppManager.stg.log_check_depth} заказов (папок)')
        
        log_frm = tb.LabelFrame(self, text='Глубина проверки лога')
        log_frm.pack(fill='both', padx=5)

        value_lbl = tb.Label(log_frm)
        value_lbl.pack(anchor='nw', padx=5)

        update_label()

        entry_var = tb.StringVar(master=log_frm)
        entry = tb.Entry(log_frm, textvariable=entry_var)

        # Рисуем лейбл раньше с позицией bottom чтобы он правильно отобразился в фрейме
        tb.Label(log_frm, text='\n'.join(msg)).pack(anchor='nw', padx=5, side='bottom')

        # Виджеты со сторонами left и right рисуем после bottom
        entry.bind('<Return>', get_entry_value)
        entry.pack(side='left', padx=5, fill='x', expand=1)

        btn = tb.Button(log_frm, text='Задать', command=get_entry_value)
        btn.pack(side='right', expand=1, fill='x', padx=(0, 5))
    

    def show_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        dir_frm = tb.LabelFrame(self, text='Рабочие директории')
        dir_frm.pack(fill='both', padx=5)
        self.show_directory_frame(dir_frm, 'Диск операторов фотопечати \'Т\'', 't_disc')
        self.show_directory_frame(dir_frm, 'Диск загрузки заказов \'Z\'', 'z_disc')
        self.show_directory_frame(dir_frm, 'Диск печати заказов \'О\'', 'o_disc')


    def show_directory_frame(self, master: tb.LabelFrame, text: str, stg_attr: str) -> None:
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
        tb.Label(master, text=text).pack(anchor='nw', padx=5)

        btn = tb.Button(
            master=master,
            text=getattr(AppManager.stg, stg_attr), 
            command=update_dir, 
            style='l_jf.TButton'
            )
        btn.pack(fill='x', padx=5, pady=(0, 5))

    def show_buttons(self):
        """Отрисовка кнопок управления"""
        lib_btn = tb.Button(
            master=self, 
            text='Библиотека', 
            width=13, 
            command=lambda: LibraryWindow()
            )
        lib_btn.pack(expand=1, anchor='s', pady=5)
