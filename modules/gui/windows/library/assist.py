from gui._source import *
from library.properties import Properties
from library.library import Product


class AssistWindow(ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    WIN_GEOMETRY = Geometry(500, 310)
    LIN_GEOMETRY = Geometry(500, 310)

    MARKS = {
        'main': 'Основное',
        'cover': 'Обложка',
        'print_mat': 'Печатный материал',
        'individual': 'Индивидуальные особенности'
        }

    def __draw_checkbutton_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор для отрисовки чек фреймов"""
        # Переменная
        self._vars[key] = var = ttk.IntVar(master)

        # Виджет
        ttk.Checkbutton(
            master, 
            text=text, 
            variable=var,
            style='success-round-toggle'
            ).pack(padx=(10, 0), pady=(27, 0))

    def __draw_combobox_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        # Рисуем название свойства
        ttk.Label(master, text=text).pack(anchor='nw', padx=(5, 0))

        # Рисуем Комбобокс
        self._vars[key] = combo = ttk.Combobox(
            master=master, 
            state='readonly', 
            values=self._properties(key),
            cursor='hand2'
            )
        combo.pack(
            anchor='nw', 
            fill='x', 
            padx=5, 
            pady=(0, 5)
            )
    
    def __draw_cover_type_radio_widgets(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        # снимаем отрисовку виджетов мастера
        for widget in master.master.winfo_children(): widget.pack_forget()

        # Формируем контейнер для правильного размещения Radiobutton'ов
        container = ttk.Frame(master.master)
        container.pack(anchor='nw', pady=(0, 5))

        # Рисуем название свойства
        ttk.Label(container, text=text).pack(anchor='nw')

        # Получаем свойства и определяем текстовую переменную 
        values = self._properties(key)
        self._vars[key] = var = ttk.StringVar(master, value=values[0])

        # Рисуем Radiobutton'ы
        for name in values:
            ttk.Radiobutton(
                master=container, 
                text=name, 
                value=name, 
                variable=var
                ).pack(
                    padx=(3, 5),
                    pady=5, 
                    anchor='nw', 
                    side='left'
                    )
        
        # Отрисовываем мастер виджеты обратно
        widgets = master.master.winfo_children()
        widgets[0].pack(anchor='n', side='right')
        widgets[1].pack(anchor='n', side='left')


    def __draw_entry_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор фрейма для отрисовки Entry виджета"""
        # Рисуем название свойства
        ttk.Label(master=master, text=text).pack(anchor='nw')

        # Текстовая переменная
        self._vars[key] = var = ttk.StringVar(master)

        # Энтри виджет
        ttk.Entry(
            master=master, 
            textvariable=var,
            ).pack(
                anchor='nw', 
                fill='x',
                padx=5,
                pady=(0, 5)
                )
    
    def __draw_full_name_widgets(self) -> None:
        """Конструктор фрейма для отрисовки Entry виджета для full_name свойства продукта"""
        # Текстовая переменная
        self._vars['full_name'] = var = ttk.StringVar(self)

        # Контейнер для виджета
        lf = ttk.LabelFrame(self, text='Полное имя продукта', padding=5)
        lf.pack(fill='x', padx=5)

        # Энтри виджет
        ttk.Entry(
            master=lf, 
            textvariable=var,
            state='disabled' if self._mode == 'change' else 'normal'
            ).pack(fill='x')

    def __draw_radio_widgets(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        # Формируем контейнер для правильного размещения Radiobutton'ов
        container = ttk.Frame(master)
        container.pack(fill='both', padx=(5, 0), pady=(0, 5))

        # Рисуем название свойства
        ttk.Label(container, text=text).pack(anchor='nw')

        # Получаем свойства и определяем текстовую переменную 
        values = self._properties(key)
        self._vars[key] = var = ttk.StringVar(master, value=values[0])

        # Рисуем Radiobutton'ы
        for name in values:
            ttk.Radiobutton(
                master=container, 
                text=name, 
                value=name, 
                variable=var
                ).pack(
                    padx=(5, 10),
                    pady=5, 
                    anchor='nw', 
                    side='left'
                    )

    FRAMES = {
        'segment': (                        # Название свойства продукта
            'main',                         # Название категории, куда будет помещен виджет
             __draw_radio_widgets,            # Cсылка на функцию для отрисовки соответствующий фреймов
             'Сегмент продукции',           # Текст для label 
             'left'                         # Позиция в мастер виджете: left или right
             ),
        'short_name': ('main', __draw_combobox_widget, 'Короткое имя', 'left'),
        'product_format': ('main', __draw_combobox_widget, 'Формат продукта', 'left'),
        'book_option': ('main', __draw_radio_widgets, 'Опция сборки книги', 'right'),
        'lamination': ('main', __draw_radio_widgets, 'Ламинация', 'right'),
        'cover_type': ('cover', __draw_cover_type_radio_widgets, 'Тип сборки обложки', 'left'),
        'carton_length': ('cover', __draw_entry_widget, 'ДЛИННА картонки', 'left'),
        'carton_height': ('cover',  __draw_entry_widget, 'ВЫСОТА картонки', 'left'),
        'cover_flap': ('cover', __draw_combobox_widget, 'Значение КЛАПАНА обложки', 'right'),
        'cover_joint': ('cover', __draw_combobox_widget, 'Значение ШАРНИРА обложки', 'right'),
        'cover_print_mat': ('print_mat', __draw_combobox_widget, 'Печатный материал обложки', 'left'),
        'page_print_mat': ('print_mat', __draw_combobox_widget, 'Печатный материал разворотов', 'right'),
        'cover_canal': ('individual', __draw_combobox_widget, "'Канал' обложки", 'left'),
        'page_canal': ('individual', __draw_combobox_widget, "'Канал' разворотов", 'right'),
        'dc_top_indent': ('individual', __draw_entry_widget, 'Отступ СВЕРХУ в мм', 'left'),
        'dc_left_indent': ('individual', __draw_entry_widget, 'Отступ СЛЕВА в мм', 'left'),
        'dc_overlap': ('individual', __draw_entry_widget, 'НАХЛЕСТ для переплета в мм', 'right'),
        'dc_break': ('individual', __draw_checkbutton_widget, 'Раскодировка с разрывом', 'right')
        }

    def __init__(
        self, 
        master: Any, 
        mode: Literal['add', 'copy', 'change'], 
        category: Type[Product], 
        product: str | None = None,
        update_func: Callable | None = None
        ) -> None:

        # Сохраняем значения в объекте
        self._mode = mode
        self._category = category
        self._properties = Properties(category.__name__)
        self._vars = {}

        # Создаем замыкание с функцией обновления
        self.write_to_library = self.write_to_library(update_func)  #type: ignore

        # Вызываем базовый класс
        super().__init__(master, product=product)

    def main(self, **kwargs) -> None:
        # Отрисовка основных фреймов
        self.set_title()
        self.__draw_full_name_widgets()
        self.draw_main_widgets()

        # Кнопка сохранить
        ttk.Button(
            self, 
            text='Сохранить', 
            width=14, 
            command=self.write_to_library   #type: ignore
            ).pack(pady=(0, 5))
        # Наполняем значениями, если продукт изменяется или копируется
        if self._mode != 'add':
            self.insert_values_from_lib_to_widgets(kwargs['product'])

    def set_title(self) -> None:
        """Установка заголовка окна"""
        match self._mode:
            case 'add': title = 'Добавление'
            case 'copy': title = 'Копирование'
            case 'change' | _ : title = 'Изменение'
        self.title(title + ' продукта: ' + self._category.__doc__)  #type: ignore

    def draw_main_widgets(self) -> None:
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        # Рисуем Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=1, padx=5, pady=5)

        # Переменная для хранения имени вкладки. 
        mark_name = None

        # Переменные для хранения фреймов, на которых будут отрисовываться виджеты
        left = right = None

        # Непосредственно, отрисовка виджетов
        for field in self._category._fields[1:]:

            # Получаем настройки виджета из словаря
            w_mark_name, draw_func, text, side = self.FRAMES[field] #type: ignore

            # Инициализируем закладку, если ее нет.
            if mark_name != w_mark_name:
                mark_name = w_mark_name
                mark = ttk.Frame(nb)
                nb.add(mark, text=self.MARKS[w_mark_name])
                
                # Инициализируем и отрисовываем левый и правый фреймы на закладке
                left = ttk.Frame(mark)
                left.pack(side='left', anchor='n')
                right = ttk.Frame(mark)
                right.pack(side='right', anchor='n')

                # Виджеты для выравнивания))
                for _side in (left, right): ttk.Frame(_side, width=242).pack(anchor='n')

            # Отрисовываем связанные виджеты 
            draw_func(self, left if side == 'left' else right, field, text)

    def insert_values_from_lib_to_widgets(self, product_name: str) -> None:
        """Метод для вставки полученных значений из бд в виджеты"""
        # Получаем продукт из библиотеки
        product = AppManager.lib.get(product_name)

        for i, attr in enumerate(product._fields):
            # Пропускаем full_name если модуль copy
            if attr == 'full_name' and self._mode == 'copy': continue

            # Размещаем значения
            self._vars[attr].set(product[i])     

    def get_values_from_widgets(self) -> Product:
        """
        Метод для получения информации из виджетов.\n
        Возвращает Product если все значения были заполнены,\n
        генерирует исключение в противном случае.
        """
        # Целочисленные значения для отдельной проверки
        numbered_var = ('carton_length', 'carton_height', 'dc_top_indent', 'dc_left_indent', 'dc_overlap')

        def _handler() -> Iterator[str | int]:
            """Обработчик переменных"""
            for key, var in self._vars.items():
                # Получаем значение
                value = var.get()

                # Генерируем исключение, если поле пустое
                if value == '': 
                    field = self.FRAMES.get(key, '"__"')[-2] if key != 'full_name' else 'Полное имя'
                    raise Exception(f'Нет данных в поле: {field}')

                # Переводим в int целочисленные значения
                if key in numbered_var: value = int(value) if value.isdigit() else 0

                yield value

        # Пакуем и возвращаем кортеж
        return self._category(*_handler())  #type: ignore

    def write_to_library(self, update_func: Callable | None) -> Callable[[], None]:
        """Ф-я для обновления/записи информации библиотеку"""
        def _func() -> None:
            # Обработчик исключений, чтобы прервать логику выполнения в случае ошибки
            try:
                # Получаем продукт
                product = self.get_values_from_widgets()

                # Обновляем или добавляем продукт в зависимости от типа обработки
                if self._mode == 'change':
                    AppManager.lib.change(product)
                    title, message = 'Изменение продукта', f'Данне успешно обновлены для:\n{product.full_name}'
                else:
                    AppManager.lib.add(product)
                    title, message = 'Добавление  продукта', f'Продукт:\n{product.full_name}\nуспешно добавлен в библиотеку'
                
                # Если была передана update_func, то обновляем виджеты
                if update_func: update_func()

                # Вывод сообщения об успехе операции
                tkmb.showinfo(title, message, parent=self)
            
            # Вывод сообщения об ошибке
            except Exception as e: tkmb.showwarning('Ошибка', str(e), parent=self)
        
        return _func