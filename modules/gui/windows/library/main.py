from ...source import *
from ....mytyping import Iterator, Type, Categories
# from .assist import AssistWindow


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
                padx=(0, 10),
                pady=(0 if i == 0 else 5, 2)
            )

            # Отрисовка виджетов продуктов
            for j, product in enumerate(products):
                p = ProductInterface(
                    self, 
                    j == len(product) - 1, 
                    category, 
                    *product
                )
                p.pack(fill=ttkc.X, padx=(0, 10))
 

class LibHeaderLabel(ttk.Frame):
    """
        Фрейм - заголовок. Повторяет функционал HeaderLabel. 
        добавляет конпку добавления продукта в библиотеку.
    """

    def __init__(self, master: LibraryWindow, product: Categories):
        self.lib_win = master
        self.product = product
        super().__init__(master.container)
        
        # Кнопка добавления продукта в библиотеку
        btn = ttk.Button(self, text='+', style='Lib+.success.Outline.TButton')
        btn.pack(side=ttkc.LEFT)

        # Лейбл с текстом
        lbl = ttk.Label(self, text=product.__doc__)     # type: ignore
        lbl.pack(anchor=ttkc.W, padx=(0, 0), side=ttkc.LEFT)


class ProductInterface(ttk.Frame):
    """Фрейм для отображения продукта и взаимодействия с ним."""
    
    def __init__(self, master: LibraryWindow, end: bool, category: Categories, id: int, name: str):
        self.lib_win = master
        self.category = category
        self.id = id
        self.name = name
        super().__init__(master.container, padding=(8, 0, 0, 0))
        self.draw_separators(end)
        lbl = ttk.Label(self, text=name, )
        lbl.pack(side=ttkc.LEFT, padx=20, pady=3)
        self.draw_buttons()
    
    def draw_separators(self, end: bool) -> None:
        """Функция для отрисовки разделителей"""
        ttk.Separator(self, orient='vertical').place(relheight=0.5 if end else 1)
        ttk.Separator(self, orient='horizontal').place(relwidth=0.98, rely=0.5)
    
    def draw_buttons(self) -> None:
        """Отрисовка кнопок взаимодействия с объектом"""
        delete = ttk.Button(self, text='🗑', style='Libdelete.danger.Outline.TButton')
        delete.pack(side=ttkc.RIGHT, padx=(0, 3))
        edit = ttk.Button(self, text='🖊', style='Libedit.warning.Outline.TButton')
        edit.pack(side=ttkc.RIGHT, padx=(0, 3))
        copy = ttk.Button(self, text='📑', style='Libcopy.success.Outline.TButton')
        copy.pack(side=ttkc.RIGHT, padx=(0, 3))






# class LibMenubutton(ttk.Menubutton):
#     """Menubutton для представления продукта в библиотеке"""
#     def __init__(self, colapsing_int: Any, text:str):
#         self._interface = colapsing_int
#         self._pname = text
#         super().__init__(
#             master=colapsing_int._lib_frame, 
#             text=text, 
#             style='ms.info.Outline.TMenubutton', 
#             cursor='hand2'
#             )
#         self.show_menu()
    
#     def delete_products(self):
#         """Удаление продукта из библиотеки"""
#         AppManager.lib.delete(self._interface._category.__name__, self._pname)
#         self._interface.update_widgets()
    
#     def show_info_box(self) -> None:
#         product = AppManager.lib.get(self._pname)
#         text = '\n'.join(f'{field} -- {getattr(product, field)}' for field in product._fields if field != 'full_name')
#         tkmb.showinfo(parent=self.master.master.master, title=product.full_name, message=text)  #type: ignore

#     def show_menu(self) -> None:
#         """Отрисовка меню"""
#         menu = ttk.Menu(self)

#         menu.add_command(
#             label='Информация', 
#             command=self.show_info_box
#             )
#         menu.add_command(
#             label='Изменить', 
#             command=lambda: AssistWindow(
#                 self._interface._lib_frame.master.master, # type: ignore
#                 mode='change',
#                 category=self._interface._category,
#                 product=self._pname,
#                 update_func=self._interface.update_widgets
#                 )
#             )
#         menu.add_command(
#             label='Копировать',
#             command=lambda: AssistWindow(
#                 self._interface._lib_frame.master.master, # type: ignore
#                 mode='copy',
#                 category=self._interface._category,
#                 product=self._pname,
#                 update_func=self._interface.update_widgets
#                 )
#             )
#         menu.add_command(label='Удалить', command=self.delete_products)
#         self['menu'] = menu


# class CollapsingInterface:
#     """Интерфейс для управления отрисовкой дочерних виджетов"""
#     __slots__ = '_row', '_lib_frame', '_category', '_container', '_state', '_btn1'

#     def __init__(self, row: int, lib_frame: ScrolledFrame, category: Type[AppManager.lib.Product]) -> None:
#         # Сохраняем атрибуты
#         self._row = row
#         self._lib_frame = lib_frame
#         self._category = category

#         # Основная кнопка С заголовком продукта и функцией свертываня / развертывания
#         self._btn1 = ttk.Button(
#             self._lib_frame,
#             text='⌄  ' + self._category.__doc__, #type: ignore
#             style='library.TButton', 
#             command=self._toggle_open_close
#             )
#         self._btn1.grid(row=self._row, column=0, sticky='ew')

#         # Вторая кнопка - добавление продукта в библиотеку
#         ttk.Button(
#             self._lib_frame, 
#             text='+' , 
#             style='LibraryPlus.TButton',
#             cursor='hand2',
#             command=self.add_product
#             ).grid(
#                 row=self._row, 
#                 column=1, 
#                 sticky='nsew', 
#                 padx=(0, 12)
#                 )
        
#         # Положение виджета для устранения проверки. False - закрыт, True - открыт
#         self._state = True

#         # контейнер для виджетов
#         self._container = ()
#         self._update_container()
    
#     def add_product(self):
#         """Добавление продукта в библиотеку"""
#         AssistWindow(
#             master=self._lib_frame.master.master, # type: ignore
#             mode='add',
#             category=self._category,
#             update_func=self.update_widgets
#             )

#     def _update_container(self) -> None:
#         """Получение кнопок по продуктам из библиотеки"""
#         def _func() -> Iterator[LibMenubutton]:
#             """Внутренний генератор для получения кнопок"""
#             for i, product in enumerate(sorted(AppManager.lib.headers[self._category]), 1):
#                 btn = LibMenubutton(self, text=product)
#                 btn.grid(
#                     row=self._row + i, 
#                     column=0, 
#                     columnspan=2, 
#                     sticky='ew',
#                     padx=(5, 17),
#                     pady=(0 if i != 1 else 5, 5)
#                 )
                
#                 yield btn
        
#         # Обновляем контейнер и сворачиваем общий фрейм
#         self._container = tuple(_func())
#         self._toggle_open_close()
 
#     def _toggle_open_close(self):
#         """Открытие и закрытие виджета"""
#         if self._state:
#             for btn in self._container: btn.grid_remove()
#             self._btn1.configure(text='⌄  ' + self._category.__doc__) #type: ignore
#         else:
#             for btn in self._container: btn.grid()
#             self._btn1.configure(text='⌃  ' + self._category.__doc__) #type: ignore
#         self._state = not self._state

#     def update_widgets(self):
#         """Обновление виджета актуальными продуктами"""
#         # Уничтожаем все виджеты в контейнере
#         for widget in self._container: widget.destroy()

#         # Получаем актуальное состояние раскрытия
#         current_state = self._state

#         # Возвращаем раскрытие к начальному состоянию
#         self._state = True

#         # Обновляем контейнер виджетов
#         self._update_container()

#         # Если виджет был открыт на момент вызова метода, то открываем его снова
#         if current_state: self._toggle_open_close()
