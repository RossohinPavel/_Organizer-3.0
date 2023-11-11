from typing import Callable, Literal, Any
from ..._source import *
from ...._appmanager import AppManager
from .assist import AssistWindow


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    width, height = 397, 351

    def main(self, *args: Any, **kwargs: Any) -> None:
        self.title('Библиотека')
        self.show_main_widget()
        self.update_treeview_values()
        self.tree.bind('<Button-3>', self.rclick_event)

    def rclick_event(self, event: tk.Event) -> None:
        """Вызов подсказки по нажатию правой кнопки"""
        row = self.tree.identify_row(event.y)
        self.tree.selection_set(row)
        if row[-1].isdigit():
            product = AppManager.lib.get(self.tree.item(row)['text'])
            text = f'{product.full_name}'                       # type: ignore # В данном случае продукт будет точно получен
            for i, fname in enumerate(product._fields[1:], 1):     # type: ignore
                text += f'\n{fname}: {product[i]}'              # type: ignore
            TipWindow(master=self, mouse_event=event, text=text)

    def show_main_widget(self) -> None:
        """Отрисовка виджетов основного меню библиотеки"""
        tk.Frame(self, width=300).grid(row=0, column=0)  # Выравнивание тривью по текущему значению
        self.tree = ttk.Treeview(self, show='tree', height=15)
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky='NSEW', rowspan=5)
        x_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.config(xscroll=x_scroll.set)  #type: ignore
        x_scroll.grid(row=6, column=0, sticky='EW')
        y_scroll = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.config(yscroll=y_scroll.set)  #type: ignore
        y_scroll.grid(row=1, column=1, sticky='NS', rowspan=5)
        MyButton(self, text='Добавить', command=self.init_lib('add')).grid(row=1, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Копировать', command=self.init_lib('copy')).grid(row=2, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Изменить', command=self.init_lib('change')).grid(row=3, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Удалить', command=self.init_lib('delete')).grid(row=4, column=2, sticky='EW', padx=2, pady=2)
        tk.Frame(self, height=200).grid(row=5, column=2)
        MyButton(self, text='Закрыть', command=self.destroy).grid(row=6, column=2, sticky='EW', rowspan=2, padx=2, pady=2)

    def update_treeview_values(self) -> None:
        """Метод для установки значений в тривью"""
        dct = {'Album': 'Полиграфические альбомы, PUR, FlexBind', 'Canvas': 'Фотохолсты',
               'Journal': 'Полиграфические фотожурналы', 'Layflat': 'Полиграфические фотокниги Layflat',
               'Photobook': 'Фотокниги на Фотобумаге', 'Photofolder': 'Фотопапки', 'Subproduct': 'Остальное'}
        for i in self.tree.get_children(''):
            self.tree.delete(i)
        for category, values in AppManager.lib.headers.items():
            cat_name = category.__name__
            rus_name = dct[cat_name]
            self.tree.insert('', 'end', iid=cat_name, text=rus_name, tags=[cat_name, rus_name])
            for i, name in enumerate(sorted(values), 1):
                self.tree.insert(cat_name, 'end', iid=f'{cat_name}{i}', text=name, tags=[cat_name, rus_name])

    def init_lib(self, module: Literal['add', 'copy', 'change', 'delete']) -> Callable[[], None]:
        """Замыкание для наделения кнопок соответствующими функциями"""
        def wrapper() -> None:
            index = self.tree.selection()
            if not index or module != 'add' and not index[0][-1].isdigit():
                tkmb.showerror(parent=self, title='Ошибка', message='Не выбрана категория или продукт')
                return
            item = self.tree.item(index[0])
            category, product = item['tags'], item['text']
            if module != 'delete':
                self.wait_window(AssistWindow(self, module=module, category=category, product=product))
            else:
                self.__delete_from_lib(category[0], product)
            self.update_treeview_values()
        return wrapper

    def __delete_from_lib(self, category: str, full_name: str) -> None:
        """Удаление продукта по выбору в тривью из библиотеки"""
        AppManager.lib.delete(category, full_name)
        tkmb.showinfo(parent=self, title="Удаление продукта", message=f'{full_name}\nУспешно удален из библиотеки')
