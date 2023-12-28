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
            category, products = val

            # Отрисовка заголовков
            lhl = LibHeaderLabel(self, category)
            lhl.pack(
                fill=ttkc.X, 
                padx=(1, 10),
                pady=(0 if i == 0 else 5, 2)
            )

            end = len(products) - 1
            # Отрисовка виджетов продуктов
            for j, product in enumerate(products):
                p = ProductInterface(
                    lhl, 
                    j == end, 
                    *product
                )
                p.pack(fill=ttkc.X, padx=(0, 10))
    
    def redraw(self) -> None:
        """Перерисовка виджетов в связи с обновлением библиотеки"""
        for widget in self.container.winfo_children():
            widget.destroy()
        self.draw_main_widgets()
 

class LibHeaderLabel(ttk.Frame):
    """
        Фрейм - заголовок. Повторяет функционал HeaderLabel. 
        добавляет конпку добавления продукта в библиотеку.
    """

    def __init__(self, master: LibraryWindow, category: Type[Categories]):
        self.lib_win = master
        self.category = category
        super().__init__(master.container)
        
        # Кнопка добавления продукта в библиотеку
        btn = ttk.Button(
            self,
            style='Lib+.success.Outline.TButton', 
            text='+', 
            command=self.add_command
        )
        btn.pack(side=ttkc.LEFT)

        # Лейбл с текстом
        lbl = ttk.Label(self, text=category.__doc__)     # type: ignore
        lbl.pack(anchor=ttkc.W, padx=(0, 0), side=ttkc.LEFT)
    
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


class ProductInterface(ttk.Frame):
    """Фрейм для отображения продукта и взаимодействия с ним."""
    
    def __init__(self, master: LibHeaderLabel, end: bool, id: int, name: str):
        self.lhl = master
        self.id = id
        super().__init__(master.master, padding=(8, 0, 0, 0))
        self.draw_separators(end)
        lbl = ttk.Label(self, text=name)
        lbl.pack(side=ttkc.LEFT, padx=20, pady=3)
        self.draw_buttons()
    
    def draw_separators(self, end: bool) -> None:
        """Функция для отрисовки разделителей"""
        ttk.Separator(self, orient='vertical').place(x=3, relheight=0.5 if end else 1)
        ttk.Separator(self, orient='horizontal').place(x=3, relwidth=0.98, rely=0.5)
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок взаимодействия с объектом"""
        delete = ttk.Button(self, text='🗑', style='Libdelete.danger.Outline.TButton')
        delete.pack(side=ttkc.RIGHT, padx=(0, 3))
        edit = ttk.Button(
            self, 
            style='Libedit.warning.Outline.TButton',
            text='🖊', 
            command=lambda: AssistWindow(self.lib_win, 'change', self.category, self.id)
        )
        edit.pack(side=ttkc.RIGHT, padx=(0, 3))
        copy = ttk.Button(
            self, 
            style='Libcopy.success.Outline.TButton',
            text='📑', 
            command=lambda: self.lhl.add_command(AppManager.lib.from_id(self.lhl.category, self.id))
        )
        copy.pack(side=ttkc.RIGHT, padx=(0, 3))
