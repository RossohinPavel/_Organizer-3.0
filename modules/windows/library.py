from .source import *


__all__ = ['LibraryWindow']


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    def __init__(self, *args, **kwargs):
        self.width, self.height = 397, 351
        super().__init__(*args, **kwargs)

    def main(self, *args, **kwargs):
        self.title('Библиотека')
        self.show_main_widget()
        self.set_treeview_values()
        self.tree.bind('<Button-3>', self.rclick_event)

    def rclick_event(self, event):
        row = self.tree.identify_row(event.y)
        self.tree.selection_set(row)
        if row[-1].isdigit():
            product = self.app_m.lib.get(self.tree.item(row)['text'])
            text = f'{product.full_name}'
            for k, v in product.__dict__.items():
                if k != 'full_name':
                    text += f'\n{k}: {v}'
            TipWindow(master=self, mouse_event=event, text=text)

    def show_main_widget(self):
        """Отрисовка виджетов основного меню библиотеки"""
        tk.Frame(self, width=300).grid(row=0, column=0)  # Выравнивание тривью по текущему значению
        self.tree = ttk.Treeview(self, show='tree', height=15)
        self.tree.grid(row=1, column=0, padx=2, pady=2, sticky='NSEW', rowspan=5)
        x_scroll = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.config(xscroll=x_scroll.set)
        x_scroll.grid(row=6, column=0, sticky='EW')
        y_scroll = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.config(yscroll=y_scroll.set)
        y_scroll.grid(row=1, column=1, sticky='NS', rowspan=5)
        MyButton(self, text='Добавить', command=self.init_lib('add')).grid(row=1, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Копировать', command=self.init_lib('copy')).grid(row=2, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Изменить', command=self.init_lib('change')).grid(row=3, column=2, sticky='EW', padx=2, pady=2)
        MyButton(self, text='Удалить', command=self.init_lib('delete')).grid(row=4, column=2, sticky='EW', padx=2, pady=2)
        tk.Frame(self, height=200).grid(row=5, column=2)
        MyButton(self, text='Закрыть', command=self.destroy).grid(row=6, column=2, sticky='EW', rowspan=2, padx=2, pady=2)

    def set_treeview_values(self):
        """Метод для установки значений в тривью"""
        for ind, obj in enumerate(self.app_m.lib.categories, 1):   # Устанавливаем категории
            self.tree.insert('', 'end', iid=obj.__name__, text=obj.rus_name, tags=obj.__name__)
        for ind, value in enumerate(sorted(self.app_m.lib.headers.items()), 1):     # Вставляем продукты в категории
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
                tkmb.showerror(parent=self, title='Ошибка', message='Не выбрана категория или продукт')
                return
            item = self.tree.item(index[0])
            category, product = item['tags'][0], item['text']
            if module != 'delete':
                self.wait_window(AssistWindow(self, module=module, category=category, product=product))
            else:
                self.__delete_from_lib(category, product)
            self.clear_treeview()
            self.set_treeview_values()
        return wrapper

    def __delete_from_lib(self, category: str, full_name: str):
        """Удаление продукта по выбору в тривью из библиотеки"""
        self.app_m.Library.delete(category, full_name)
        tkmb.showinfo(parent=self, title="Удаление продукта", message=f'{full_name}\nУспешно удален из библиотеки')


class AssistWindow(ChildWindow):
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

    def __init__(self, *args, **kwargs):
        dct = {'Album': (498, 528), 'Canvas': (498, 278), 'Journal': (498, 278), 'Layflat': (498, 425),
               'Photobook': (498, 488), 'Photofolder': (498, 381), 'Subproduct': (498, 238)}
        self.module = kwargs.pop('module')
        self.category = kwargs.pop('category')
        self.product = kwargs.pop('product')
        self.width, self.height = dct[self.category]
        self.product_vars = {}  # Словарь для хранения переменных виджетов
        self.product_obj = None
        super().__init__(*args, **kwargs)

    def main(self, *args, **kwargs):
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
                kwargs.update({'values': self.product_obj.__dict__[frm], 'padx': 1.48, **sides[side].pop(0)})
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
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = var = tk.StringVar(master=container)
        entry = ttk.Entry(master=frame, width=kwargs.get('width', 39), textvariable=var,
                          state='disabled' if key == 'full_name' and self.module == 'change' else 'normal')
        entry.pack()
        frame.grid(row=kwargs.get('row', 0), column=kwargs.get('column', 0), padx=kwargs.get('padx', 0))

    def __show_radio(self, key, container, **kwargs):
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        pos = [{'row': 1, 'column': i} for i in range(5)]
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).grid(row=0, column=0, columnspan=3, sticky='nw')
        self.product_vars[key] = var = tk.StringVar(master=container, value=kwargs['values'][0])
        for name in kwargs['values']:
            ttk.Radiobutton(master=frame, text=name, value=name, variable=var).grid(**pos.pop(0), sticky='ew')
        frame.grid(row=kwargs['row'], column=kwargs['column'], sticky='ew', padx=kwargs.get('padx', 0))

    def __show_combobox(self, key, container, **kwargs):
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = ttk.Combobox(master=frame, width=kwargs.get('width', 36),
                                              state='readonly', values=kwargs['values'])
        self.product_vars[key].pack(anchor='nw', padx=0.5)
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def __show_check(self, key, container, **kwargs):
        """Конструктор для отрисовки чек фреймов"""
        frame = tk.Frame(master=container)
        self.product_vars[key] = var = tk.IntVar(master=container)
        ttk.Checkbutton(master=frame, text=kwargs['text'], variable=var).pack()
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def show_buttons(self):
        """Функция для отрисовки кнопок"""
        text = {'add': 'Добавить', 'copy': 'Добавить', 'change': 'Изменить'}[self.module]
        frame = tk.Frame(self, height=28)
        MyButton(frame, text=text, width=30, command=self.write_to_library).place(x=130, y=0)
        MyButton(frame, text='Закрыть', width=10, command=self.destroy).place(x=415, y=0)
        frame.pack(expand=1, fill='x')

    def insert_values_from_lib(self):
        """Метод для вставки полученных значений в бд"""
        for key, value in self.app_m.Library.get(self.product).__dict__.items():
            if key == 'full_name' and self.module == 'copy':
                continue
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
            tkmb.showwarning(parent=self, title='Проверка на дубликат',
                             message=f'Добавляемый продукт:\n{self.product_obj.full_name}\nуже есть в библиотеке')
            return
        if self.module == 'change':
            self.app_m.Library.change(self.product_obj)
            tkmb.showinfo(parent=self, title='Изменение продукта',
                          message=f'Данне успешно обновлены для:\n{self.product_obj.full_name}')
        else:
            self.app_m.Library.add(self.product_obj)
            tkmb.showinfo(parent=self, title='Добавление  продукта',
                          message=f'Продукт:\n{self.product_obj.full_name}\nуспешно добавлен в библиотеку')
