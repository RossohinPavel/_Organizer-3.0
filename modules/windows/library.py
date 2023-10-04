import modules.windows.source as source
from modules.windows.frames import LabeledFrame


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
        for ind, obj in enumerate(self.app_m.lib.categories, 1):   # Устанавливаем категории
            self.tree.insert('', 'end', iid=obj.__name__, text=obj.rus_name, tags=obj.__name__)
        for ind, value in enumerate(self.app_m.Library.headers.items(), 1):     # Вставляем продукты в категории
            name, category = value
            self.tree.insert(str(category), 'end', iid=f'{category}{ind}', text=name, tags=category)

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
            if not index or module != 'add' and not index[0][-1].isdigit():
                source.tkmb.showerror(parent=self, title='Ошибка', message='Не выбрана категория или продукт')
                return
            item = self.tree.item(index[0])
            args = item['tags'][0], item['text']
            if module != 'delete':
                self.wait_window(AssistWindow(self, module, *args))
            else:
                self.__delete_from_lib(*args)
            self.clear_treeview()
            self.set_treeview_values()
        return wrapper

    def __delete_from_lib(self, category: str, full_name: str):
        """Удаление продукта по выбору в тривью из библиотеки"""
        self.app_m.Library.delete(category, full_name)
        source.tkmb.showinfo(parent=self, title="Удаление продукта",
                             message=f'{full_name}\nУспешно удален из библиотеки')


class AssistWindow(source.ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    __FRAMES = {'segment': ('options', 'radio', 'left', {'text': 'Выберите сегмент продукции'}),
                'short_name': ('options', 'combo', 'left', {'text': 'Выберите короткое имя'}),
                'product_format': ('options', 'combo', 'left', {'text': 'Выберите формат продукта'}),
                'book_option': ('options', 'radio', 'right', {'text': 'Выберите опции сборки книги'}),
                'lamination': ('options', 'radio', 'right', {'text': 'Выберите ламинацию для продукта'}),
                'cover_type': ('cover_type', 'radio', 'left',  {}),
                'carton_length': ('cover_val', 'entry', 'left', {'text': 'Укажите ДЛИННУ картонки'}),
                'carton_height': ('cover_val',  'entry', 'left', {'text': 'Укажите ВЫСОТУ картонки'}),
                'cover_clapan': ('cover_val', 'combo', 'right', {'text': 'Укажите значения КЛАПАНА'}),
                'cover_joint': ('cover_val', 'combo', 'right', {'text': 'Укажите значения ШАРНИРА'}),
                'cover_print_mat': ('print_mat', 'combo', 'left', {'text': 'Выберите печатный материал обложки'}),
                'page_print_mat': ('print_mat', 'combo', 'right', {'text': 'Выберите печатный материал разворотов'}),
                'cover_canal': ('individual', 'combo', 'left', {'text': "Выберите 'канал' обложки"}),
                'page_canal': ('individual', 'combo', 'right', {'text': "Выберите 'канал' разворотов"}),
                'dc_top_indent': ('individual', 'entry', 'left', {'text': 'Введите значение отступа СВЕРХУ в мм'}),
                'dc_left_indent': ('individual', 'entry', 'left', {'text': 'Введите значение отступа СЛЕВА в мм'}),
                'dc_overlap': ('individual', 'entry', 'right', {'text': 'НАХЛЕСТ для переплета в мм'}),
                'dc_break': ('individual', 'check', 'right', {'text': 'Раскодировка с разрывом'})
                }

    def __init__(self, parent_root, module, category, product):
        self.module = module
        self.category = category
        self.product = product
        self.product_vars = {}  # Словарь для хранения переменных виджетов
        self.product_obj = None
        super().__init__(parent_root)

    def main(self):
        self.title({'add': 'Добавление продукта', 'copy': 'Копирование продукта', 'change': 'Изменение продукта'}[self.module])
        self.product_obj = self.app_m.Library.get_blank(self.category)
        self.show_main_widgets()
        if self.module != 'add':
            self.insert_values_from_lib()
        self.show_buttons()

    def show_main_widgets(self):
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        # Рисуем Фуллнейм независимо от основной логики отрисовки виджетов
        self.__show_entry('full_name', self.show_m_frame('Введите полное имя продукта')().container, **{'width': 80})
        mf = {'options': self.show_m_frame('Общие особенности продукта'),
              'cover_type': self.show_m_frame('Тип сборки обложки'),
              'cover_val': self.show_m_frame('Особенности сборки обложки'),
              'print_mat': self.show_m_frame('Печатный материал'),
              'individual': self.show_m_frame('Индивидуальные особенности продукта')}
        funcs = {'entry': self.__show_entry, 'radio': self.__show_radio,
                 'combo': self.__show_combobox, 'check': self.__show_check}
        sides = {'left': [], 'right': []}
        for frm in self.__FRAMES:
            if frm in self.product_obj.__dict__:
                m_name, child, side, kwargs = self.__FRAMES[frm]
                if not isinstance(mf[m_name], LabeledFrame):
                    mf[m_name] = mf[m_name]()
                    sides['left'] = [{'row': i, 'column': 0} for i in range(3)]
                    sides['right'] = [{'row': i, 'column': 1} for i in range(3)]
                kwargs.update({'values': self.product_obj.__dict__[frm], 'padx': 1.3, **sides[side].pop(0)})
                funcs[child](frm, mf[m_name].container, **kwargs)

    def show_m_frame(self, text):
        """Замыкание для отрисовки мастер-фреймов"""
        def wrapper():
            frame = LabeledFrame(master=self, text=text)
            frame.pack(expand=1, fill='x')
            return frame
        return wrapper

    def __show_entry(self, key, container, **kwargs):
        """Конструктор фрейма для отрисовки Entry виджета"""
        frame = source.tk.Frame(master=container)
        if 'text' in kwargs:
            source.ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = var = source.tk.StringVar(master=container)
        entry = source.ttk.Entry(master=frame, width=kwargs.get('width', 39), textvariable=var,
                                 state='disabled' if key == 'full_name' and self.module == 'change' else 'normal')
        entry.pack()
        frame.grid(row=kwargs.get('row', 0), column=kwargs.get('column', 0), padx=kwargs.get('padx', 0))

    def __show_radio(self, key, container, **kwargs):
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        pos = [{'row': 1, 'column': i} for i in range(5)]
        frame = source.tk.Frame(master=container)
        if 'text' in kwargs:
            source.ttk.Label(master=frame, text=kwargs['text']).grid(row=0, column=0, columnspan=3, sticky='nw')
        self.product_vars[key] = var = source.tk.StringVar(master=container, value=kwargs['values'][0])
        for name in kwargs['values']:
            radio = source.ttk.Radiobutton(master=frame, text=name, value=name, variable=var)
            radio.grid(**pos.pop(0), sticky='ew')
        frame.grid(row=kwargs['row'], column=kwargs['column'], sticky='ew', padx=kwargs.get('padx', 0))

    def __show_combobox(self, key, container, **kwargs):
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        frame = source.tk.Frame(master=container)
        if 'text' in kwargs:
            source.ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = source.ttk.Combobox(master=frame, width=kwargs.get('width', 36),
                                                     state='readonly', values=kwargs['values'])
        self.product_vars[key].pack(anchor='nw')
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def __show_check(self, key, container, **kwargs):
        """Конструктор для отрисовки чек фреймов"""
        frame = source.tk.Frame(master=container)
        self.product_vars[key] = var = source.tk.IntVar(master=container)
        chbtn = source.ttk.Checkbutton(master=frame, text=kwargs['text'], variable=var)
        chbtn.pack()
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def show_buttons(self):
        """Функция для отрисовки кнопок"""
        text = {'add': 'Добавить', 'copy': 'Добавить', 'change': 'Изменить'}[self.module]
        frame = source.tk.Frame(self, height=28)
        func_button = source.MyButton(frame, text=text, width=30, command=self.write_to_library)
        func_button.place(x=130, y=0)
        close_button = source.MyButton(frame, text='Закрыть', width=10, command=self.destroy)
        close_button.place(x=415, y=0)
        frame.pack(expand=1, fill='x')

    def insert_values_from_lib(self):
        """Метод для вставки полученных значений в бд"""
        for key, value in self.app_m.Library.get(self.product).__dict__.items():
            self.product_vars[key].set(value)

    def get_values_from_widgets(self) -> bool:
        """Метод для получения информации из менюшек и установки их в product_obj
        Возвращает True если все значения были заполнены, False в противном случае"""
        numbered_var = ('carton_length', 'carton_height', 'dc_top_indent',
                        'dc_left_indent', 'dc_overlap')
        for key, var in self.product_vars.items():
            value = var.get()
            if value == '':
                return False
            if key in numbered_var:
                value = int(value) if value.isdigit() else 0
            self.product_obj.__dict__[key] = value
        return True

    def write_to_library(self):
        """Ф-я для обновления/записи информации библиотеку"""
        if not self.get_values_from_widgets():
            return
        if self.module != 'change' and not self.app_m.Library.check_unique(self.product_obj):
            source.tkmb.showwarning(parent=self, title='Проверка на дубликат',
                                    message=f'Добавляемый продукт:\n{self.product_obj.full_name}\nуже есть в библиотеке')
            return
        if self.module == 'change':
            self.app_m.Library.change(self.product_obj)
            source.tkmb.showinfo(parent=self, title='Изменение продукта',
                                 message=f'Данне успешно обновлены для:\n{self.product_obj.full_name}')
        else:
            self.app_m.Library.add(self.product_obj)
            source.tkmb.showinfo(parent=self, title='Добавление  продукта',
                                 message=f'Продукт:\n{self.product_obj.full_name}\nуспешно добавлен в библиотеку')
