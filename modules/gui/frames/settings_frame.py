from ..source import *
from ..source.style import style_init
from ..windows import LibraryWindow


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
        light = (
            'cosmo', 'flatly', 'journal', 'litera', 'lumen', 'minty', 
            'pulse', 'sandstone', 'united', 'yeti', 'morph', 'simplex', 'cerculean'
        )

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

        HeaderLabel(theme_frame, text='Тема', anchor='n').place(x=0, y=0, relwidth=1)

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
        theme_btn.place(x=0, y=15, relwidth=1)

        # Добавление вызова в Дескриптор тем
        AppManager.desc.theme.add_call(lambda v: theme_btn.configure(text=v))      #type: ignore

        # Свитчер палитр
        palette_frame = ttk.Frame(container, height=44)
        palette_frame.pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 3))
        ttk.Frame(container, height=44).pack(fill=ttkc.X, side=ttkc.LEFT, expand=1, padx=(3, 0))

        HeaderLabel(palette_frame, text='Палитра', anchor='n').place(x=0, y=0, relwidth=1)

        def theme_switch(theme: str) -> None:
            """Переключает тему в меню"""
            menu = self.dark_menu
            if theme == 'light':
                menu = self.light_menu
            palette_btn.configure(menu=menu)    #type: ignore
            if AppManager.desc.color._value:    #type: ignore
                menu.invoke(0)                  #type: ignore

        palette_btn = ttk.Menubutton(palette_frame, style='ts.Outline.TMenubutton')
        palette_btn.place(x=0, y=15, relwidth=1)

        # Добавление вызова в Дескриптор тем и палитр
        AppManager.desc.theme.add_call(theme_switch)                               #type: ignore
        AppManager.desc.color.add_call(lambda v: palette_btn.configure(text=v))    #type: ignore
        AppManager.desc.color.add_call(lambda v: style_init(v))                    #type: ignore

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
            style='btn.TButton', 
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
        HeaderLabel(self, text).pack(anchor=ttkc.W, fill=ttkc.X, pady=(0, 3))
        btn = SettingLine(self, lambda: self._update_dir(attr))
        btn.pack(padx=5, pady=(0, 15), anchor=ttkc.W)

        # Добавление вызова дескриптору
        add_call_func = eval(f'AppManager.desc.{attr}.add_call')
        add_call_func(lambda e: btn.var.set(e))

    def _update_dir(self, attr: str) -> None:
        """Получение информации из файлового диалога"""
        path = tkfd.askdirectory(
            parent=AppManager.mw, 
            initialdir=getattr(AppManager.stg, attr), 
            title=f'Выберите расположение'
        )
        if path:
            setattr(AppManager.stg, attr, path)
