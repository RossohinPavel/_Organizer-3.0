import modules.windows.source as source


class LibraryWindow(source.ChildWindow):
    def __init__(self, parent_root):
        super().__init__(parent_root)
        self.title('Библиотека')
        self.tree = None
        # self.lib = Library()
        self.show_main_widget()
        self.resizable(False, False)
        # self.set_treeview_values()
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
        add_btn = source.MyButton(self, text='Добавить', command=self.add_to_lib)
        add_btn.grid(row=1, column=2, sticky=source.tk.EW, padx=2, pady=2)
        copy_btn = source.MyButton(self, text='Копировать', command=self.copy_from_lib)
        copy_btn.grid(row=2, column=2, sticky=source.tk.EW, padx=2, pady=2)
        change_btn = source.MyButton(self, text='Изменить', command=self.change_lib)
        change_btn.grid(row=3, column=2, sticky=source.tk.EW, padx=2, pady=2)
        del_btn = source.MyButton(self, text='Удалить', command=self.delete_from_lib)
        del_btn.grid(row=4, column=2, sticky=source.tk.EW, padx=2, pady=2)
        y_leveler = source.tk.Frame(self, height=200)
        y_leveler.grid(row=5, column=2)
        close_btn = source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.grid(row=6, column=2, sticky=source.tk.EW, rowspan=2, padx=2, pady=2)

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        key_index = 1
        for key, values in self.lib.get_product_names().items():
            self.tree.insert('', Source.tk.END, iid=key_index, text=self.lib.translator(key))
            for index, value in enumerate(values):
                self.tree.insert(key_index, Source.tk.END, iid=int(f'{key_index}{index}'), text=value, tags=key)
            key_index += 1

    def get_treeview_values(self) -> tuple | None:
        """Метод для получения данных из виджета. Возвращает кортеж (название таблицы в бд, имя)"""
        index = self.tree.selection()
        if not index or len(index[0]) == 1:
            return
        item = self.tree.item(index[0])
        return item['tags'][0], item['text']

    def clear_treeview(self):
        """Очитска тривью от содержимого"""
        for i in self.tree.get_children(''):
            self.tree.delete(i)

    def add_to_lib(self):
        AddToLibWindow(self)
        self.clear_treeview()
        self.set_treeview_values()
        self.focus()

    def copy_from_lib(self):
        product = self.get_treeview_values()
        if product:
            CopyFromLibWindow(self, product)
            self.clear_treeview()
            self.set_treeview_values()
        self.focus()

    def change_lib(self):
        product = self.get_treeview_values()
        if product:
            ChangeLibWindow(self, product)
        self.focus()

    def delete_from_lib(self):
        """Удаление продукта по выбору в тривью из библиотеки"""
        values = self.get_treeview_values()
        if not values:
            return
        self.lib.delete(*values)
        self.clear_treeview()
        self.set_treeview_values()
        Source.tkmb.showinfo(title="Удаление продукта", message=f'{values[1]}\nУспешно удален из библиотеки')
