from ...source import *
from ....mytyping import Categories, Type
from .assist import AssistWindow


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    width = 550
    height = 400
    win_title = 'Библиотека'

    def __init__(self) -> None:
        super().__init__()
        self.container = ScrolledFrame(self, bootstyle='round')
        self.container.pack(fill=ttkc.BOTH, expand=1)
        self.draw_main_widgets()
       
    def draw_main_widgets(self) -> None:
        """Отрисовка основных виджетов на основе полученной из библиотеки информации"""
        for i, val in enumerate(AppManager.lib.get_headers().items()):
            # Отрисовка интерфейса заголовка
            category, products = val
            h = HeaderFrame(self, category)
            h.pack(fill=ttkc.X, padx=(1, 10), pady=(0 if i == 0 else 5, 2))
            h.draw_bound_widgets(products)

    def redraw(self) -> None:
        """Перерисовка виджетов в связи с обновлением библиотеки"""
        for widget in self.container.winfo_children():
            widget.destroy()
        self.draw_main_widgets()
 

class HeaderFrame(ttk.Frame):
    """
        Фрейм - заголовок. Повторяет функционал HeaderLabel. 
        добавляет конпку добавления продукта в библиотеку.
    """

    def __init__(self, master: LibraryWindow, category: Type[Categories]) -> None:
        super().__init__(master.container)

        # Сохраняем ссылку на LibraryWindow и категорию продукта
        self.lib_win = master
        self.category = category

        # Отрисовка основных виджетов и зависимых
        self.draw_main_widgets()
    
    def draw_main_widgets(self) -> None:
        """Отрисовка основных виджетов заголовка"""
        
        # Кнопка добавления продукта в библиотеку
        btn = ttk.Button(
            self,
            style='Lib+.success.Outline.TButton', 
            text='+', 
            command=self.add_command
        )
        btn.pack(side=ttkc.LEFT)

        # Лейбл с текстом
        lbl = ttk.Label(self, text=self.category.__doc__)       # type: ignore
        lbl.pack(anchor=ttkc.W, padx=(0, 0), side=ttkc.LEFT)
    
    def draw_bound_widgets(self, products: list[tuple[int, str]]) -> None:
        """Отрисовка связанных виджетов по значениям из products"""
        end = len(products) - 1
        for j, product in enumerate(products):
            p = ProductFrame(
                self.lib_win, 
                j == end, 
                self.category, 
                *product
            )
            p.pack(fill=ttkc.X, padx=(0, 10))
    
    def add_command(self, base=None) -> None:
        """Добавление нового продукта в библиотеку."""
        if base:
            name = f'Копия {base.name}'
            values = base[1:]
        else:
            name = f'Новый {self.category.__name__}'
            prop_obj = AppManager.lib.properties(self.category.__name__)
            values = (prop_obj(x)[0] for x in self.category._fields[1:])
        try: 
            AppManager.lib.add(self.category(name, *values)) #type: ignore
            self.lib_win.redraw()
        except Exception as e: 
            tkmb.showwarning('Ошибка', str(e), parent=self.lib_win)


class ProductFrame(ttk.Frame):
    """Фрейм для отображения продукта и взаимодействия с ним."""
    
    def __init__(
        self, 
        master: LibraryWindow, 
        end: bool,                  # Маркер для отрисовки половины виджета Separator
        category: Type[Categories],
        id: int, 
        name: str
        ) -> None:
        super().__init__(master.container, padding=(8, 0, 0, 0))

        # Сохраняем нужные атрибуты
        self.lib_win = master
        self.category = category
        self.id = id

        # Отрисовка основных виджетов
        self.draw_separators(end)
        ttk.Label(self, text=name).pack(side=ttkc.LEFT, padx=20, pady=3)
        self.draw_buttons()
    
    def draw_separators(self, end: bool) -> None:
        """Функция для отрисовки разделителей"""
        ttk.Separator(self, orient='vertical').place(x=3, relheight=0.5 if end else 1)
        ttk.Separator(self, orient='horizontal').place(x=3, relwidth=0.98, rely=0.5)
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок взаимодействия с объектом"""
        delete = ttk.Button(
            self,
            style='Libdelete.danger.Outline.TButton',
            text='🗑', 
            command=self.delete_command
        )
        delete.pack(side=ttkc.RIGHT, padx=(0, 3))
        edit = ttk.Button(
            self, 
            style='Libedit.warning.Outline.TButton',
            text='🖊', 
            command=lambda: AssistWindow(self.lhl, 'change', self.lhl.category, self.id)
        )
        edit.pack(side=ttkc.RIGHT, padx=(0, 3))
        copy = ttk.Button(
            self, 
            style='Libcopy.success.Outline.TButton',
            text='📑', 
            command=lambda: self.lhl.add_command(AppManager.lib.from_id(self.lhl.category, self.id))
        )
        copy.pack(side=ttkc.RIGHT, padx=(0, 3))
    
    def delete_command(self) -> None:
        """Удаление продукта из библиотеки"""
        AppManager.lib.delete(self.category, self.id)
        self.lib_win.redraw()
