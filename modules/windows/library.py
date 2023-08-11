import modules.windows.source as source


class LibraryWindow(source.ChildWindow):
    """Окно управления библиотекой"""

    def main(self):
        self.title('Библиотека')
        self.show_main_widget()
        self.set_treeview_values()

    def show_main_widget(self):
        """Отрисовка виджетов основного меню библиотеки"""
        x_leveler = source.tk.Frame(self, width=300)  # Выравнивание тривью по текущему значению
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
            key = self.library.product_gen.translator(key)
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

        def wrapper():
            index = self.tree.selection()
            if not index or module != 'add' and len(index[0]) < 2:
                source.tkmb.showerror(parent=self, title='Ошибка', message='Не выбрана категория или продукт')
                return
            args = self.convert_item(module, self.tree.item(index[0]))
            if module != 'delete':
                self.wait_window(AssistWindow(self, module, *args))
            else:
                self.__delete_from_lib(*args)
            self.clear_treeview()
            self.set_treeview_values()

        return wrapper

    @staticmethod
    def convert_item(module: str, item: dict) -> tuple:
        """Вспомогательная функция, формирующая нужный для объекта module аргумент"""
        args = (item['text'],)
        if module == 'add' and item['tags']:
            args = (' '.join(item['tags']),)
        if module != 'add':
            args = (' '.join(item['tags']),) + args
        return args

    def __delete_from_lib(self, category: str, full_name: str):
        """Удаление продукта по выбору в тривью из библиотеки"""
        self.library.delete(category, full_name)
        source.tkmb.showinfo(parent=self, title="Удаление продукта",
                             message=f'{full_name}\nУспешно удален из библиотеки')


class AssistWindow(source.ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    __FRAMES = {'full_name': ('entry', 'Введите полное имя продукта', 2, 0, {'width': 80}),
                'segment': ('radio', 'Выберите сегмент продукции', 2, 41),
                'short_name': ('combo', 'Выберите короткое имя', 2, 82),
                'product_format': ('combo', 'Выберите формат продукта', 2, 123),
                'book_option': ('radio', 'Выберите опции сборки книги', 250, 82),
                'lamination': ('radio', 'Выберите ламинацию для продукта', 250, 41),
                'cover_type': ('radio', 'Выберите тип обложки', 2, 169),
                'carton_length': ('entry', 'Укажите ДЛИННУ и ВЫСОТУ картонки', 252, 169, {'width': 18}),
                'carton_height': ('entry', None, 372, 169, {'width': 18}),
                'cover_clapan': ('combo', 'Укажите значения КЛАПАНА и ШАРНИРА', 252, 210, {'width': 15}),
                'cover_joint': ('combo', None, 372, 210, {'width': 15}),
                'cover_print_mat': ('combo', 'Выберите печатный материал обложки', 2, 255),
                'page_print_mat': ('combo', 'Выберите печатный материал разворотов', 250, 255),
                'cover_canal': ('combo', "Выберите 'канал' обложки", 2, 300),
                'page_canal': ('combo', "Выберите 'канал' разворотов", 250, 300),
                'dc_top_indent': ('entry', 'Введите значение отступа СВЕРХУ в мм', 2, 300),
                'dc_left_indent': ('entry', 'Введите значение отступа СЛЕВА в мм', 2, 341),
                'dc_overlap': ('entry', 'НАХЛЕСТ для переплета в мм', 250, 300),
                'dc_break': ('check', 'Раскодировка с разрывом', 250, 355)
                }

    def __init__(self, parent_root, module, category, product=''):
        self.module = module
        self.category = category
        self.product = product
        self.product_vars = {}  # Словарь для хранения переменных виджетов
        self.product_dict = None  # Переменная для хранения словаря продукта
        super().__init__(parent_root)

    def main(self):
        self.product_dict = self.library.product_gen(self.category, True)
        self.show_header()
        self.show_main_widgets()
        if self.module != 'add':
            self.insert_values_from_lib()
        self.show_buttons()

    def show_header(self):
        """Изменение заголовка окна и отрисовка головного виджета"""
        st = {'add': 'Добавление продукта', 'copy': 'Копирование продукта', 'change': 'Изменение продукта'}[self.module]
        self.title(st)
        frame = source.tk.Frame(self)
        label1 = source.ttk.Label(frame, text=st + ' в категорию:' if self.module != 'change' else st + ' в категории:')
        label1.pack(side='left', padx=2, pady=2)
        label2 = source.ttk.Label(frame, text=self.category, relief='solid', justify='center')
        label2.pack(side='right', padx=2, pady=2, ipadx=2, ipady=2)
        frame.pack()
        separator = source.tk.Frame(self, width=487, height=1, bg='black')
        separator.pack(padx=2)

    def show_main_widgets(self):
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        frame = source.tk.Frame(self, height=385)
        funcs = {'entry': self.__show_entry_frame, 'radio': self.__show_radio_frame,
                 'combo': self.__show_combobox_frame, 'check': self.__show_check_frame}
        for x, y in ((0, 167), (0, 254), (0, 299)):  # Рисуем разделители для отделения тематических блоков
            separator = source.tk.Frame(frame, width=496, height=1, bg='black')
            separator.place(x=x, y=y)
        for key, values in self.product_dict.items():
            current_frame, *args = self.__FRAMES[key]
            kwargs = {'values': values}
            if isinstance(args[-1], dict):
                kwargs.update(args[-1])
                args = args[:-1]
            funcs[current_frame](key, frame, *args, **kwargs)
        frame.pack(expand=True, fill='both')

    def show_buttons(self):
        """Функция для отрисовки кнопок"""
        text = {'add': 'Добавить', 'copy': 'Копировать', 'change': 'Изменить'}[self.module]
        frame = source.tk.Frame(self, width=487, height=30)
        func_button = source.MyButton(frame, text=text, width=30, command=self.write_to_library)
        func_button.place(x=140, y=2)
        close_button = source.MyButton(frame, text='Закрыть', width=10, command=self.destroy)
        close_button.place(x=407, y=2)
        frame.pack()

    @staticmethod
    def __show_label(container, text, x, y):
        """Конструктор текстового лейбла"""
        if text:
            label = source.ttk.Label(master=container, text=text)
            label.place(x=x, y=y)

    def __show_entry_frame(self, key, container, text, x, y, **kwargs):
        """Конструктор фрейма для отрисовки Entry виджета"""
        self.__show_label(container, text, x, y)
        self.product_vars[key] = var = source.tk.StringVar(master=container)
        entry = source.ttk.Entry(master=container, width=kwargs.get('width', 39), textvariable=var,
                                 state='disabled' if key == 'full_name' and self.module == 'change' else 'normal')
        entry.place(x=x, y=y + 20)

    def __show_radio_frame(self, key, container, text, x, y, **kwargs):
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        self.__show_label(container, text, x, y)
        self.product_vars[key] = var = source.tk.StringVar(master=container, value=kwargs['values'][0])
        indent = {'segment': ((0, 20), (80, 20)), 'cover_type': ((0, 20), (0, 40), (0, 60), (80, 20), (80, 40)),
                  'book_option': ((0, 20), (50, 20), (100, 20)), 'lamination': ((0, 20), (50, 20), (100, 20))}[key]
        for i, name in enumerate(kwargs['values']):
            i_x, i_y = indent[i]
            x_pos, y_pos = x + i_x, y + i_y
            radio = source.ttk.Radiobutton(master=container, text=name, value=name, variable=var)
            radio.place(x=x_pos, y=y_pos)

    def __show_combobox_frame(self, key, container, text, x, y, **kwargs):
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        self.__show_label(container, text, x, y)
        self.product_vars[key] = source.ttk.Combobox(master=container, width=kwargs.get('width', 36),
                                                     state='readonly', values=kwargs['values'])
        self.product_vars[key].place(x=x, y=y + 20)

    def __show_check_frame(self, key, container, text, x, y, **kwargs):
        """Конструктор для отрисовки чек фреймов"""
        self.product_vars[key] = var = source.tk.IntVar(master=container)
        check_btn = source.ttk.Checkbutton(master=container, text=text, variable=var)
        check_btn.place(x=x, y=y)

    def insert_values_from_lib(self):
        """Метод для вставки полученных значений в бд"""
        for key, value in self.library.get_product_values(self.category, self.product).items():
            self.product_vars[key].set(value)

    def get_values_from_widgets(self) -> bool:
        """Метод для получения информации из менюшек и установки их в словарь product_dict
        Возвращает True если все значения были заполнены, False в противном случае"""
        numbered_var = ('carton_length', 'carton_height', 'cover_clapan', 'cover_joint', 'dc_top_indent',
                        'dc_left_indent', 'dc_overlap', 'dc_break')
        for key, var in self.product_vars.items():
            value = var.get()
            if value == '':
                return False
            if key in numbered_var:
                value = int(value) if value.isdigit() else 0
            self.product_dict[key] = value
        return True

    def write_to_library(self):
        if not self.get_values_from_widgets():
            return
        if self.module != 'change' and not self.library.check_unique(self.product_dict.category(), self.product_dict['full_name']):
            source.tkmb.showwarning(parent=self, title='Проверка на дубликат',
                                    message=f'Добавляемый продукт:\n{self.product_dict["full_name"]}\nуже есть в библиотеке')
            return
        if self.module == 'change':
            self.library.change(self.product_dict)
            source.tkmb.showinfo(parent=self, title='Изменение продукта',
                                 message=f'Данне успешно обновлены для:\n{self.product_dict["full_name"]}')
        else:
            self.library.add(self.product_dict)
            source.tkmb.showinfo(parent=self, title='Добавление  продукта',
                                 message=f'Продукт:\n{self.product_dict["full_name"]}\nуспешно добавлен в библиотеку')
