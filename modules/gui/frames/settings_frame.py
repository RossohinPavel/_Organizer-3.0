from ..source import *
from ...descriptors import Z_disc, O_disc, T_disc, Theme, Color
from ...mytyping import Callable
from ..windows.library import LibraryWindow


class SettingsFrame(ttk.Frame):
    """Фрейм основных настроек приложения"""

    def __init__(self, master: Any):
        super().__init__(master, padding=5)
        self.dark_menu = self.light_menu = None
        self.init_color_menus()
        self.draw_theme_widgets()
        self.draw_library_widgets()
        self.draw_directory_widgets()

    def theme_closure(self, name: str) -> Callable:
        """Замыкание для смены тем"""
        return lambda: setattr(AppManager.stg, 'color', name)

    def init_color_menus(self) -> None:
        dark = ('solar', 'superhero', 'darkly', 'cyborg', 'vapor')
        light = ('cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean')

        self.dark_menu = ttk.Menu(self)
        for name in dark:
            self.dark_menu.add_command(
                label=f'  {name}'.ljust(29, ' '),
                command=self.theme_closure(name)
            )
        self.light_menu = ttk.Menu(self)
        for name in light:
            self.light_menu.add_command(
                label=f'  {name}'.ljust(29, ' '),
                command=self.theme_closure(name)
            )
    
    def draw_theme_widgets(self) -> None:
        HeaderLabel(self, 'Оформление').pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))

        container = ttk.Frame(self, padding=(5, 0, 5, 15))
        container.pack(fill=ttkc.X)

        # Свитчер тем
        theme_frame = ttk.Frame(container, height=44)
        theme_frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(0, 3))

        HeaderLabel(theme_frame, text='Тема:').place(x=0, y=0, relwidth=1)

        theme_menu = ttk.Menu(theme_frame)
        theme_menu.add_command(
            label='  light', 
            command=lambda: setattr(AppManager.stg, 'theme', 'light')
        )
        theme_menu.add_command(
            label='  dark', 
            command=lambda: setattr(AppManager.stg, 'theme', 'dark')
            )
        theme_btn = ttk.Menubutton(theme_frame, menu=theme_menu, style='ts.Outline.TMenubutton')
        theme_btn.place(x=0, y=18, relwidth=1)

        # Добавление вызова в Дескриптор тем
        Theme.add_call(lambda v: theme_btn.configure(text=v))   #type: ignore

        # Свитчер палитр
        palette_frame = ttk.Frame(container, height=44)
        palette_frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 3))
        ttk.Frame(container, height=44).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 0))

        HeaderLabel(palette_frame, text='Палитра:').place(x=0, y=0, relwidth=1)

        def theme_switch(theme: str) -> None:
            """Переключает тему в меню"""
            menu = self.dark_menu
            if theme == 'light':
                menu = self.light_menu
            palette_btn.configure(menu=menu)  #type: ignore
            if Color._value:
                menu.invoke(0)              #type: ignore

        palette_btn = ttk.Menubutton(palette_frame, style='ts.Outline.TMenubutton')
        palette_btn.place(x=0, y=18, relwidth=1)

        # Добавление вызова в Дескриптор тем и палитр
        Theme.add_call(theme_switch)
        Color.add_call(lambda v: palette_btn.configure(text=v))   #type: ignore
        Color.add_call(lambda v: style_init(v))

    def draw_library_widgets(self) -> None:
        """Отрисовка виджетов библиотеки"""
        HeaderLabel(self, 'Настройка библиотеки').pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))

        container = ttk.Frame(self, padding=(5, 0, 5, 15))
        container.pack(fill=ttkc.X)

        frame = ttk.Frame(container, height=25)
        frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(0, 3))
        ttk.Frame(container, height=25).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 3))
        ttk.Frame(container, height=25).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 0))

        btn = ttk.Button(
            frame, 
            style='minibtn.Outline.TButton', 
            text='Библиотека', 
            command=lambda: LibraryWindow()
        )
        btn.place(x=0, y=0, relwidth=1)

    def draw_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.draw_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc')
        self.draw_directory_frame('Диск печати заказов \'О\'', 'o_disc')
        self.draw_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc')

    def draw_directory_frame(self, text: str, attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        HeaderLabel(self, text).pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 2))
        btn = ttk.Button(self, style='l_jf.Outline.TButton', command=lambda: self._update_dir(attr))
        btn.pack(fill=ttkc.X, pady=(0, 15), padx=5)

        # Добавление вызова дескриптору
        add_call_func = eval(f'{attr.capitalize()}.add_call')
        add_call_func(lambda e: btn.configure(text=e))

    def _update_dir(self, attr: str) -> None:
        """Получение информации из файлового диалога"""
        path = tkfd.askdirectory(
            parent=AppManager.mw, 
            initialdir=getattr(AppManager.stg, attr), 
            title=f'Выберите расположение'
        )
        if path:
            setattr(AppManager.stg, attr, path)

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
