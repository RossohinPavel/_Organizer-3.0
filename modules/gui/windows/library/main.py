from ...source import *
from ...source import images
# from .assist import AssistWindow, Type


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    width = 550
    height = 400
    win_title = 'Библиотека'

    def __init__(self) -> None:
        super().__init__()
        self.container = ScrolledFrame(self, bootstyle='round')
        self.container.pack(fill=ttkc.BOTH, expand=1)
        self.draw_header()
        self.draw_main_widgets()

    def draw_main_widgets(self) -> None:
        """Отрисовка основных виджетов на основе полученной из библиотеки информации"""
        # Создаем словарь на основе полученных из библиотеки продуктов
        headers = AppManager.lib.get_headers()
        headers.sort()

        dct = {}
        for type, name in headers:
            if type not in dct: 
                dct[type] = []
            dct[type].append(name)

        # Отрисовка виджетов
        for type, lst in dct.items():
            h = HeaderLabel(self.container, type, padx=5)
            h.pack(anchor=ttkc.W, pady=(10, 3))

            for i, name in enumerate(lst, start=1):
                p = ProductFrame(self.container, i == len(lst), name)
                p.pack(fill=ttkc.X, padx=(10, 10))

    def redraw(self) -> None:
        """Перерисовка виджетов в связи с обновлением библиотеки"""
        for widget in self.container.winfo_children():
            widget.destroy()
        self.draw_main_widgets()
    
    def draw_header(self) -> None:
        """Ф-я для отрисовки заголовка, с подсказкой, где находится кнопка добавления продукта."""
        btn = ttk.Button(self, text='Добавить', style='btn.success.TButton')
        btn.place(anchor=ttkc.N, relx=0.5, y=3, width=80)

    
#     def add_command(self, base=None) -> None:
#         """Добавление нового продукта в библиотеку."""
#         if base:
#             name = f'Копия {base.name}'
#             values = base[1:]
#         else:
#             name = f'Новый {self.category.__name__}'
#             prop_obj = AppManager.lib.properties(self.category.__name__)
#             values = (prop_obj(x)[0] for x in self.category._fields[1:])
#         try: 
#             AppManager.lib.add(self.category(name, *values)) #type: ignore
#             self.lib_win.redraw()
#         except Exception as e: 
#             tkmb.showwarning('Ошибка', str(e), parent=self.lib_win)


class ProductFrame(ttk.Frame):
    """Фрейм для отображения продукта и взаимодействия с ним."""
    
    def __init__(self, master: Any, end: bool, name: str) -> None:
        super().__init__(master)

        # Сохраняем нужные атрибуты
        self._maseter = master
        self.name = name

        # Отрисовка основных виджетов
        self.draw_separators(end)
        ttk.Label(self, text=name).pack(side=ttkc.LEFT, padx=20, pady=3)
        self.draw_buttons()
    
    def draw_separators(self, end: bool) -> None:
        """Функция для отрисовки разделителей"""
        ttk.Separator(self, orient='vertical').place(relheight=0.5 if end else 1)
        ttk.Separator(self, orient='horizontal').place(relwidth=0.98, rely=0.5)
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок взаимодействия с объектом"""
        delete = ttk.Button(
            self,
            style='image.danger.TButton',
            image=images.DELETE,
            command=self.delete_command
        )
        delete.pack(side=ttkc.RIGHT, padx=(0, 3))
        edit = ttk.Button(
            self, 
            style='image.warning.TButton',
            image=images.EDIT,
            command=self.change_command
        )
        edit.pack(side=ttkc.RIGHT, padx=(0, 3))
        copy = ttk.Button(
            self, 
            style='image.success.TButton',
            image=images.COPY,
            command=self.copy_command
        )
        copy.pack(side=ttkc.RIGHT, padx=(0, 3))

    def change_command(self) -> None:
        """Изменение продукта в библиотеке"""
        args = self.header_frame.lib_win, self.header_frame.category, self.id
        AssistWindow(*args)
    
    def copy_command(self) -> None:
        """Копирование продукта"""
        product = AppManager.lib.from_id(self.header_frame.category, self.id)
        self.header_frame.add_command(product)
    
    def delete_command(self) -> None:
        """Удаление продукта из библиотеки"""
        AppManager.lib.delete(self.header_frame.category, self.id)
        self.header_frame.lib_win.redraw()
