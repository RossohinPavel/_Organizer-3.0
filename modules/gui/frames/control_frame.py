from ..source import *
from ...descriptors import Z_disc, O_disc, T_disc, Theme, Color
from ...mytyping import Callable
from ..windows.library import LibraryWindow


class ControlFrame(ttk.Frame):
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
        HeaderLabel(self, 'Оформление').pack(anchor=ttkc.W, fill=ttkc.X)

        # Контейнер для виджетов
        container = ttk.Frame(self)
        container.pack(padx=5, anchor=ttkc.W, pady=(0, 15))

        # Свитчер тем
        ttk.Label(container, text='Тема:').grid(row=0, column=0, sticky=ttkc.W)

        theme_menu = ttk.Menu(container)
        theme_menu.add_command(
            label='  light' + ' '*29, 
            command=lambda: setattr(AppManager.stg, 'theme', 'light')
        )
        theme_menu.add_command(
            label='  dark', 
            command=lambda: setattr(AppManager.stg, 'theme', 'dark')
            )
        theme_btn = ttk.Menubutton(container, menu=theme_menu, style='ts.Outline.TMenubutton')
        theme_btn.grid(row=1, column=0)

        # Добавление вызова в Дескриптор тем
        Theme.add_call(lambda v: theme_btn.configure(text=v))   #type: ignore

        # Свитчер палитр
        ttk.Label(container, text='Палитра:').grid(row=0, column=1, sticky=ttkc.W, padx=10)

        def theme_switch(theme: str) -> None:
            """Переключает тему в меню"""
            menu = self.dark_menu
            if theme == 'light':
                menu = self.light_menu
            color_btn.configure(menu=menu)  #type: ignore
            if Color._value:
                menu.invoke(0)              #type: ignore

        color_btn = ttk.Menubutton(container, style='ts.Outline.TMenubutton')
        color_btn.grid(row=1, column=1, padx=10)

        Theme.add_call(theme_switch)
        Color.add_call(lambda v: color_btn.configure(text=v))   #type: ignore
        Color.add_call(lambda v: style_init(v))

    def draw_library_widgets(self) -> None:
        """Отрисовка виджетов библиотеки"""
        HeaderLabel(self, 'Настройка библиотеки').pack(anchor=ttkc.W, fill=ttkc.X)
        btn = ttk.Button(
            self, 
            style='minibtn.Outline.TButton', 
            text='Библиотека', 
            width=19,
            command=lambda: LibraryWindow()
        )
        btn.pack(pady=(0, 15), padx=5, anchor=ttkc.W)

    def draw_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.draw_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc')
        self.draw_directory_frame('Диск печати заказов \'О\'', 'o_disc')
        self.draw_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc')

    def draw_directory_frame(self, text: str, attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        HeaderLabel(self, text).pack(anchor=ttkc.W, fill=ttkc.X)
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
