import modules.windows.source as source


class LibraryWindow(source.ChildWindow):
    """Окно управления библиотекой"""
    def main(self):
        self.title('Библиотека')
        self.show_main_widget()
        self.set_treeview_values()

    def show_main_widget(self):
        """Отрисовка виджетов основного меню библиотеки"""
        x_leveler = source.tk.Frame(self, width=300)    # Выравнивание тривью по текущему значению
        x_leveler.grid(row=0, column=0)
        self.tree = source.ttk.Treeview(self, show='tree', height=15)
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky='NSEW', rowspan=5)
        x_scroll = source.ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.config(xscroll=x_scroll.set)
        x_scroll.grid(row=6, column=0, sticky='EW')
        y_scroll = source.ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.config(yscroll=y_scroll.set)
        y_scroll.grid(row=1, column=1, sticky='NS', rowspan=5)
        add_btn = source.MyButton(self, text='Добавить', command=None)
        add_btn.grid(row=1, column=2, sticky='EW', padx=2, pady=2)
        copy_btn = source.MyButton(self, text='Копировать', command=None)
        copy_btn.grid(row=2, column=2, sticky='EW', padx=2, pady=2)
        change_btn = source.MyButton(self, text='Изменить', command=None)
        change_btn.grid(row=3, column=2, sticky='EW', padx=2, pady=2)
        del_btn = source.MyButton(self, text='Удалить', command=None)
        del_btn.grid(row=4, column=2, sticky='EW', padx=2, pady=2)
        y_leveler = source.tk.Frame(self, height=200)
        y_leveler.grid(row=5, column=2)
        close_btn = source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.grid(row=6, column=2, sticky='EW', rowspan=2, padx=2, pady=2)

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        key_index = 1
        for key, values in self.library.get_product_headers().items():
            self.tree.insert('', source.tk.END, iid=key_index, text=key)
            for index, value in enumerate(values):
                self.tree.insert(key_index, source.tk.END, iid=int(f'{key_index}{index}'), text=value, tags=key)
            key_index += 1
