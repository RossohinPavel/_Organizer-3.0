import modules.windows.source as source


class LibraryWindow(source.ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Библиотека')
        self.tree = None
        self.show_main_widget()
        self.resizable(False, False)
        self.to_parent_center()
        self.library = parent_root.library
        self.set_treeview_values()

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        key_index = 1
        for key, values in self.library.get_product_headers().items():
            self.tree.insert('', source.tk.END, iid=key_index, text=self.library.product.translator(key))
            for index, value in enumerate(values):
                self.tree.insert(key_index, source.tk.END, iid=int(f'{key_index}{index}'), text=value, tags=key)
            key_index += 1

    def clear_treeview(self):
        """Очитска тривью от содержимого"""
        for i in self.tree.get_children(''):
            self.tree.delete(i)

    def get_treeview_values(self) -> tuple | None:
        """Метод для получения данных из виджета. Возвращает кортеж (название таблицы в бд, имя)"""
        index = self.tree.selection()
        if not index or len(index[0]) == 1:
            return
        item = self.tree.item(index[0])
        return item['tags'][0], item['text']

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
        value = self.get_treeview_values()
        if value is None:
            return
        CopyFromLibWindow(self, category=value[0], product=value[1])

    def init_change_lib(self):
        value = self.get_treeview_values()
        if value is None:
            return
        ChangeLibWindow(self, category=value[0], product=value[1])

    def init_delete_from_lib(self):
        """Удаление продукта по выбору в тривью из библиотеки"""
        values = self.get_treeview_values()
        if not values:
            return
        self.library.delete(*values)
        self.clear_treeview()
        self.set_treeview_values()
        source.tkmb.showinfo(title="Удаление продукта", message=f'{values[1]}\nУспешно удален из библиотеки')


class AssistWindow(source.ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""

    def __init__(self, parent_root, category=None, product=None):
        super().__init__(parent_root)
        self.library = parent_root.library
        self.product_obj = None
        self.category_combobox = self.show_category_frame(category)
        self.product_menus_frame = self.show_product_menus_frame()
        self.func_button = self.show_buttons()
        self.main()
        self.to_parent_center()
        self.resizable(False, False)

    def main(self):
        """Абстрактная функция для отрисовки основных виджетов окон"""
        pass

    def show_category_frame(self, category):
        """Отрисовка комбобокса. Возвращает ссылку на его объект"""
        label = source.ttk.Label(self, text='Выберите категорию')
        label.pack()
        combobox = source.ttk.Combobox(self, state='disabled', width=40, values=self.library.product._rusnames)
        combobox.pack()
        if category:
            combobox.set(self.library.product.translator(category))
        separator = source.tk.Canvas(self, width=496, height=1, bg='black')
        separator.pack()
        return combobox

    def show_product_menus_frame(self):
        """Отрисовка контейнера для менюшек. Возвращает ссылку на этот объект"""
        frame = source.tk.Frame(self, width=500, height=380)
        frame.pack()
        return frame

    def show_buttons(self):
        """Отрисовка контейнера для кнопок и сами кнопки. Возвращает ссылку на основную кнопку"""
        frame = source.tk.Frame(self, width=500, height=30)
        func_button = source.MyButton(frame, text='text', width=30)
        func_button.place(x=140, y=2)
        close_button = source.MyButton(frame, text='Закрыть', width=10, command=self.destroy)
        close_button.place(x=418, y=2)
        frame.pack()
        return func_button

    def init_menu_lines(self, event=None):
        self.product_obj = self.library.product(self.category_combobox.get())
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        frames = {}
        self.__show_ef(0, 0, 'text', 0, 0)

    def __show_ef(self, obj, attr, text, x, y, ef_width=39, ef_state='normal'):
        label = source.ttk.Label(master=self.product_menus_frame, text=text)
        label.place(x=x, y=y)
        entry = source.ttk.Entry(master=self.product_menus_frame, width=ef_width, state=ef_state)
        entry.place(x=x, y=y+20)
        entry.bind('<Control-KeyPress>', lambda x: print('ssss'))


class AddToLibWindow(AssistWindow):
    """Окно для добавления продукта в библиотеку"""
    def main(self):
        self.title('Добавление продукта в Библиотеку')
        self.category_combobox.config(state='readonly')
        self.category_combobox.bind('<<ComboboxSelected>>', self.init_menu_lines)
        self.func_button.config(command=lambda: print(self.product_obj.__dict__))


class CopyFromLibWindow(AssistWindow):
    """Окно для создания нового продукта на основе имеющегося"""
    def main(self):
        self.title('Копирование продукта')
        self.init_menu_lines()


class ChangeLibWindow(CopyFromLibWindow):
    """Окно для внесения изменения в продукт"""
    def main(self):
        super().main()
        self.title('Изменение продукта')
