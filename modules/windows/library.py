import modules.windows.source as source
from modules.library.products import Product as Product


class LibraryWindow(source.ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Библиотека')
        self.tree = None
        self.show_main_widget()
        self.resizable(False, False)
        self.to_parent_center()

    def show_main_widget(self):
        """Отрисовка виджетов основного меню библиотеки"""
        x_leveler = source.tk.Frame(self, width=300)    # Выравнивание тривью по текущему значению
        x_leveler.grid(row=0, column=0)
        self.tree = source.ttk.Treeview(self, show='tree', height=15)
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky=source.tk.NSEW, rowspan=5)
        x_scroll = source.ttk.Scrollbar(self, orient=source.tk.HORIZONTAL, command=self.tree.xview)
        self.tree.config(xscroll=x_scroll.set)
        x_scroll.grid(row=6, column=0, sticky=source.tk.EW)
        y_scroll = source.ttk.Scrollbar(self, orient=source.tk.VERTICAL, command=self.tree.yview)
        self.tree.config(yscroll=y_scroll.set)
        y_scroll.grid(row=1, column=1, sticky=source.tk.NS, rowspan=5)
        add_btn = source.MyButton(self, text='Добавить', command=self.init_add_to_lib)
        add_btn.grid(row=1, column=2, sticky=source.tk.EW, padx=2, pady=2)
        copy_btn = source.MyButton(self, text='Копировать', command=self.init_copy_from_lib)
        copy_btn.grid(row=2, column=2, sticky=source.tk.EW, padx=2, pady=2)
        change_btn = source.MyButton(self, text='Изменить', command=self.init_change_lib)
        change_btn.grid(row=3, column=2, sticky=source.tk.EW, padx=2, pady=2)
        del_btn = source.MyButton(self, text='Удалить', command=self.init_delete_from_lib)
        del_btn.grid(row=4, column=2, sticky=source.tk.EW, padx=2, pady=2)
        y_leveler = source.tk.Frame(self, height=200)
        y_leveler.grid(row=5, column=2)
        close_btn = source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.grid(row=6, column=2, sticky=source.tk.EW, rowspan=2, padx=2, pady=2)

    def init_add_to_lib(self):
        AddToLibWindow(self)

    def init_copy_from_lib(self):
        CopyFromLibWindow(self)

    def init_change_lib(self):
        ChangeLibWindow(self)

    def init_delete_from_lib(self):
        pass


class AssistWindow(source.ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.category_combobox = self.show_category_frame()
        self.main()
        self.to_parent_center()
        self.resizable(False, False)

    def main(self):
        """Абстрактная функция для отрисовки основных виджетов окон"""
        pass

    def show_category_frame(self):
        """Отрисовка комбобокса. Возвращает ссылку на его объект"""
        label = source.ttk.Label(self, text='Выберите категорию')
        label.pack()
        combobox = source.ttk.Combobox(self, state='readonly', width=40, values=Product._rnames)
        combobox.pack()
        separator = source.tk.Canvas(self, width=496, height=1, bg='black')
        separator.pack()
        return combobox


class AddToLibWindow(AssistWindow):
    """Окно для добавления продукта в библиотеку"""
    def main(self):
        self.title('Добавление продукта в Библиотеку')


class CopyFromLibWindow(AssistWindow):
    """Окно для создания нового продукта на основе имеющегося"""
    def main(self):
        self.title('Копирование продукта')


class ChangeLibWindow(AssistWindow):
    """Окно для внесения изменения в продукт"""
    def main(self):
        self.title('Изменение продукта')