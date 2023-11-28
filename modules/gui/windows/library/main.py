from ..._source import *
from .assist import AssistWindow


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    WIN_GEOMETRY = Geometry(450, 500)
    LIN_GEOMETRY = Geometry(450, 500)
    win_title = 'Библиотека'

    def __init__(self, /, **kwargs) -> None:
        super().__init__(AppManager.mw, **kwargs)
        scroled_frame = ScrolledFrame(self, bootstyle='round', padding=5)
        scroled_frame.pack(fill='both', expand=1)
        # Установка новых виджетов
        for category in AppManager.lib.headers:
            frame = CategoryLabelFrame(scroled_frame, category)
            frame.pack(fill='both', expand=1, padx=(0, 10), pady=(0, 5))


class CategoryLabelFrame(tb.LabelFrame):
    """Фрейм отображения категории продукции в библиотеке"""

    def __init__(self, lib_frame: ScrolledFrame, category: Type[AppManager.lib.products]) -> None:
        # Сохраняем категорию
        self._category = category
        # Инициализируем виджет
        super().__init__(
            master=lib_frame, 
            text=' ' * 8 + category.__doc__,    #type: ignore
            height=40,
            padding=(5, 5, 5, 0)
            )
        self.update_product_widgets()
    
    def add_product(self):
        self.wait_window(AssistWindow(
            master=self.master.master.master, # type: ignore
            mode='add',
            category=self._category
            ))   
        self.update_product_widgets()
        
    def update_product_widgets(self) -> None:
        """Обновление виждета. Отрисовка актуальных виджетов продуктов"""
        # Уничтожаем все виджеты
        for widget in self.winfo_children():
            widget.destroy()
        # Рисуем актуальные виджеты
        self.show_add_button()
        for product in sorted(AppManager.lib.headers[self._category]):
            LibMenubutton(self, text=product).pack(fill='x', pady=(0, 5))

    def show_add_button(self) -> None:
        """Отрисовка кнопки + на виджете"""
        add_btn = tb.Button(
            master=self, 
            text='+', 
            style='miniplus.success.Outline.TButton', 
            cursor='hand2',
            command=self.add_product
            )
        add_btn.place(x=5, y=-23)


class LibMenubutton(tb.Menubutton):
    """Menubutton для представления продукта в библиотеке"""
    def __init__(self, lib_frame: CategoryLabelFrame, text:str):
        self._cat_frame = lib_frame
        self._pname = text
        super().__init__(
            master=lib_frame, 
            text=text, 
            style='ms.info.Outline.TMenubutton', 
            cursor='hand2'
            )
        self.show_menu()
    
    def delete_products(self):
        """Удаление продукта из библиотеки"""
        AppManager.lib.delete(self._cat_frame._category.__name__, self._pname)
        self._cat_frame.update_product_widgets()
    
    def show_info_box(self) -> None:
        product = AppManager.lib.get(self._pname)
        text = '\n'.join(f'{field} -- {getattr(product, field)}' for field in product._fields if field != 'full_name')
        tkmb.showinfo(parent=self.master.master.master, title=product.full_name, message=text)  #type: ignore

    def show_menu(self) -> None:
        """Отрисовка меню"""
        menu = tb.Menu(self)
        menu.add_command(label='Информация', command=self.show_info_box)
        menu.add_command(label='Изменить')
        menu.add_command(label='Копировать')
        menu.add_command(label='Удалить', command=self.delete_products)
        self['menu'] = menu
