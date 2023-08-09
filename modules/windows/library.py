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
        add_btn = source.MyButton(self, text='Добавить', command=self.init_lib('add'))
        add_btn.grid(row=1, column=2, sticky='EW', padx=2, pady=2)
        copy_btn = source.MyButton(self, text='Копировать', command=self.init_lib('copy'))
        copy_btn.grid(row=2, column=2, sticky='EW', padx=2, pady=2)
        change_btn = source.MyButton(self, text='Изменить', command=self.init_lib('change'))
        change_btn.grid(row=3, column=2, sticky='EW', padx=2, pady=2)
        del_btn = source.MyButton(self, text='Удалить', command=self.init_lib('delete'))
        del_btn.grid(row=4, column=2, sticky='EW', padx=2, pady=2)
        y_leveler = source.tk.Frame(self, height=200)
        y_leveler.grid(row=5, column=2)
        close_btn = source.MyButton(self, text='Закрыть', command=self.destroy)
        close_btn.grid(row=6, column=2, sticky='EW', rowspan=2, padx=2, pady=2)

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        key_index = 1
        for key, values in self.library.get_product_headers().items():
            self.tree.insert('', 'end', iid=str(key_index), text=key)
            for index, value in enumerate(values):
                self.tree.insert(str(key_index), source.tk.END, iid=f'{key_index}{index}', text=value, tags=key)
            key_index += 1

    def clear_treeview(self):
        """Очитска тривью от содержимого"""
        for i in self.tree.get_children(''):
            self.tree.delete(i)

    def init_lib(self, module: str):
        """Замыкание для наделения кнопок соответствующими функциями
        :param module: 'add', 'copy', 'change' или 'delete'
        :return: Функцию, соответствующую module
        """
        funcs = {'add': lambda *args: print(args), 'copy': lambda *args: print(args),
                 'change': lambda *args: print(args), 'delete': self.__delete_from_lib}

        def wrapper():
            index = self.tree.selection()
            if not index or module != 'add' and len(index[0]) < 2:
                source.tkmb.showerror(parent=self, title='Ошибка', message='Не выбрана категория или продукт')
                return
            funcs[module](*self.convert_item(module, self.tree.item(index[0])))
            self.clear_treeview()
            self.set_treeview_values()
        return wrapper

    @staticmethod
    def convert_item(module: str, item: dict) -> tuple:
        """Вспомогательная функция, формирующая нужный для объекта module аргумент"""
        args = (item['text'], )
        if module == 'add' and item['tags']:
            args = (' '.join(item['tags']), )
        if module != 'add':
            args = (' '.join(item['tags']), ) + args
        return args

    def __delete_from_lib(self, category: str, full_name: str):
        """Удаление продукта по выбору в тривью из библиотеки"""
        self.library.delete(category, full_name)
        source.tkmb.showinfo(parent=self, title="Удаление продукта", message=f'{full_name}\nУспешно удален из библиотеки')


class AssistWindow(source.ChildWindow):
    def main(self):
        pass


class AddToLibWindow(AssistWindow):
    pass

