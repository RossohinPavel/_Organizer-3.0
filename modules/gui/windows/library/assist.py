from gui._source import *
from library.properties import Properties
from library.library import Product


class AssistWindow(ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""

    @staticmethod
    def __get_main_frame(text: str) -> Callable[[Any], tb.LabelFrame]:
        """Замыкание для получения мастер-фреймов"""
        def wrapper(master: Any) -> tb.LabelFrame:
            return tb.LabelFrame(master=master, text=text, padding=(5, 0, 5, 5))
        return wrapper


    MAIN_FRAMES = {
        'full_name': __get_main_frame('Полное имя продукта'),
        'options': __get_main_frame('Общие особенности продукта'),
        'cover_type': __get_main_frame('Тип сборки обложки'),
        'cover_val': __get_main_frame('Технические размеры обложки'),
        'print_mat': __get_main_frame('Печатный материал'),
        'individual': __get_main_frame('Индивидуальные особенности продукта')
        }

    
    @staticmethod
    def __get_checkbutton_widget(instance: Any, key: str, master: tb.Frame, text: str) -> tb.Checkbutton:
        """Конструктор для отрисовки чек фреймов"""
        # Переменная
        instance._vars[key] = var = tb.IntVar(master)
        ch_btn = tb.Checkbutton(master, text=text, variable=var)
        return ch_btn


    @staticmethod
    def __get_combobox_widget(instance: Any, key: str, master: tb.Frame, text: str) -> tb.Frame:
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        # Формируем контейнер
        frame = tb.Frame(master)
        # Рисуем название свойства
        tb.Label(frame, text=text).pack(anchor='nw')
        # Рисуем Комбобокс
        instance._vars[key] = combo = tb.Combobox(
            master=frame, 
            state='readonly', 
            values=instance._properties(key),
            cursor='hand2'
            )
        combo.pack(anchor='nw', fill='x')
        return frame


    @staticmethod
    def __get_entry_widget(instance: Any, key: str, master: tb.Frame, text: str) -> tb.Frame:
        """Конструктор фрейма для отрисовки Entry виджета"""
        # Формируем контейнер
        frame = tb.Frame(master)
        # Рисуем название свойства
        tb.Label(master=frame, text=text).pack(anchor='nw')
        # Текстовая переменная
        instance._vars[key] = var = tb.StringVar(master)
        # Энтри виджет
        entry = tb.Entry(
            master=frame, 
            textvariable=var,
            state='disabled' if key == 'full_name' and instance._mode == 'change' else 'normal')
        entry.pack(anchor='nw', fill='x')
        return frame


    @staticmethod
    def __get_full_name_entry_widget(instance: Any, key: str, master: tb.Frame, _) -> tb.Entry:
        """Конструктор фрейма для отрисовки Entry виджета"""
        # Текстовая переменная
        instance._vars[key] = var = tb.StringVar(master)
        # Энтри виджет
        entry = tb.Entry(
            master=master, 
            textvariable=var,
            state='disabled' if key == 'full_name' and instance._mode == 'change' else 'normal'
            )
        return entry
    

    @staticmethod
    def __get_radio_widget(instance: Any, key: str, master: tb.Frame, text: str) -> tb.Frame:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        # Формируем контейнер
        frame = tb.Frame(master)
        # Рисуем название свойства
        tb.Label(frame, text=text).pack(anchor='nw')
        # Получаем свойства и определяем текстовую переменную 
        values = instance._properties(key)
        instance._vars[key] = var = tb.StringVar(master, value=values[0])
        # Рисуем Radiobutton
        for name in values:
            tb.Radiobutton(
                master=frame, 
                text=name, 
                value=name, 
                variable=var
                ).pack(side='left', padx=(5, 10))
        return frame


    @staticmethod
    def __get_cover_type_widget(instance: Any, key: str, master: tb.Frame, text: str) -> tb.Frame:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        # Формируем контейнер
        frame = tb.Frame(master)
        # Получаем свойства и определяем текстовую переменную 
        values = instance._properties(key)
        instance._vars[key] = var = tb.StringVar(master, value=values[0])
        # Рисуем Radiobutton
        for name in values:
            tb.Radiobutton(
                master=frame, 
                text=name, 
                value=name, 
                variable=var
                ).pack(side='left', padx=(5, 5))
        return frame


    FRAMES = {
        'full_name': (                      # Название свойства продукта
            'full_name',                    # Название категории, для отрисовки LabelFrame
            __get_full_name_entry_widget,   # Cсылка на функцию для отрисовки соответствующий фреймов
            'left',                         # Позиция в мастер виджете: left или right
            ''                              # Текст для label 
            ),
        'segment': ('options', __get_radio_widget, 'left', 'Сегмент продукции'),
        'short_name': ('options', __get_combobox_widget, 'left', 'Короткое имя'),
        'product_format': ('options', __get_combobox_widget, 'left','Формат продукта'),
        'book_option': ('options', __get_radio_widget, 'right', 'Опция сборки книги'),
        'lamination': ('options', __get_radio_widget, 'right', 'Ламинация'),
        'cover_type': ('cover_type', __get_cover_type_widget, 'left',  'Тип сборки обложки'),
        'carton_length': ('cover_val', __get_entry_widget, 'left', 'ДЛИННА картонки'),
        'carton_height': ('cover_val',  __get_entry_widget, 'left', 'ВЫСОТА картонки'),
        'cover_flap': ('cover_val', __get_combobox_widget, 'right','Значение КЛАПАНА обложки'),
        'cover_joint': ('cover_val', __get_combobox_widget, 'right','Значение ШАРНИРА обложки'),
        'cover_print_mat': ('print_mat', __get_combobox_widget, 'left', 'Печатный материал обложки'),
        'page_print_mat': ('print_mat', __get_combobox_widget, 'right', 'Печатный материал разворотов'),
        'cover_canal': ('individual', __get_combobox_widget, 'left',"'Канал' обложки"),
        'page_canal': ('individual', __get_combobox_widget, 'right', "'Канал' разворотов"),
        'dc_top_indent': ('individual', __get_entry_widget, 'left', 'Отступ СВЕРХУ в мм'),
        'dc_left_indent': ('individual', __get_entry_widget, 'left', 'Отступ СЛЕВА в мм'),
        'dc_overlap': ('individual', __get_entry_widget, 'right', 'НАХЛЕСТ для переплета в мм'),
        'dc_break': ('individual', __get_checkbutton_widget, 'right', 'Раскодировка с разрывом')
        }


    def __init__(self, master: Any, mode: Literal['add', 'copy', 'change'], category: Type[Product], product: Product | None = None) -> None:
        # Сохраняем значения в объекте
        self._mode = mode
        self._category = category
        self._product = product
        self._properties = Properties(category.__name__)
        self._vars = {}
        super().__init__(master)

    
    def get_geometry_by_system(self) -> Geometry:
        # Переопределенный метод выдаст размер окна относительно обрабатываемого продукта
        match AppManager.SYSTEM:     
            case 'win':
                match self._category.__name__:
                    case 'Album': y = 528
                    case 'Canvas': y = 278
                    case 'Journal': y = 278
                    case 'Layflat': y = 425
                    case 'Photobook': y = 488
                    case 'Photofolder': y = 381
                    case 'Subproduct' | _: y = 238
                return Geometry(498, y)
            case 'lin' | _:
                match self._category.__name__:
                    case 'Album': y = 664
                    case 'Canvas': y = 350
                    case 'Journal': y = 350
                    case 'Layflat': y = 530
                    case 'Photobook': y = 612
                    case 'Photofolder': y = 484
                    case 'Subproduct' | _: y = 298
                return Geometry(498, y)
        

    def main(self, **kwargs) -> None:
        self.set_title()
        self.show_main_widgets()
        self.show_buttons()
    #     if self.module != 'add':
    #         self.insert_values_from_lib_to_widgets(product)

    def set_title(self) -> None:
        """Установка заголовка окна"""
        match self._mode:
            case 'add': title = 'Добавление'
            case 'copy': title = 'Копирование'
            case 'change' | _ : title = 'Изменение'
        self.title(title + ' продукта: ' + self._category.__doc__)  #type: ignore


    def show_main_widgets(self) -> None:
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        main_frame_name = main_frame = None
        # Словарь для хранения информации для разделения виджетов по сторонам
        sides = {'left': [], 'right': []}
        # Непосредственно, отрисовка виджетов
        for field in self._category._fields:
            master_name, child, side, text = self.FRAMES[field]
            # Инициализируем мастер фрейм, если его еще нет
            if master_name != main_frame_name:
                main_frame_name = master_name
                main_frame = self.MAIN_FRAMES[master_name](self)
                main_frame.pack(fill='x', padx=5, pady=(0, 5))
                # Очищаем и заново наполняем стороны размещения виджетов
                sides['left'].clear() ; sides['right'].clear()
                sides['left'].extend({'row': i, 'column': 0} for i in range(4))
                sides['right'].extend({'row': i, 'column': 1} for i in range(4))
                # Рисуем фреймы для выравнивания виджетов
                if main_frame_name not in ('full_name', 'cover_type'):
                    tb.Frame(main_frame, height=1, width=250).grid(sides['left'].pop(0))
                    tb.Frame(main_frame, height=1, width=250).grid(sides['right'].pop(0))
            # Получаем сторону для размещения
            grid_side = sides[side].pop(0)
            # Настраиваем на полное растяжение к краям
            main_frame.columnconfigure(grid_side['column'], weight=1)   #type: ignore
            main_frame.rowconfigure(grid_side['column'], weight=1)      #type: ignore
            # Формируем выравнивание по х относительно стороны размещения
            padx = 0
            if main_frame_name not in ('full_name', 'cover_type'):
                padx = (0, 3) if side == 'left' else (3, 0)
            # Отрисовываем дочерние виджеты
            child(self, field, main_frame, text).grid(**grid_side, padx=padx, sticky='ew')


    def show_buttons(self) -> None:
        """Функция для отрисовки кнопок"""
        tb.Button(self, text='Сохранить', width=14, command=lambda: print(self.winfo_geometry())).pack(pady=(0, 5))


    # def insert_values_from_lib_to_widgets(self, product_name: str) -> None:
    #     """Метод для вставки полученных значений из бд в виджеты"""
    #     product = AppManager.lib.get(product_name)
    #     for i, attr in enumerate(product._fields):      # type: ignore      # Продукт точно вернется
    #         if attr == 'full_name' and self.module == 'copy': continue
    #         self.product_vars[attr].set(product[i])     # type: ignore


    # def get_values_from_widgets(self) -> Product:
    #     """Метод для получения информации из виджетов.\n
    #     Возвращает Product если все значения были заполнены,\n
    #     генерирует исключение в противном случае."""
    #     numbered_var = ('carton_length', 'carton_height', 'dc_top_indent', 'dc_left_indent', 'dc_overlap')
    #     def handler() -> Iterator[str | int]:
    #         for key, var in self.product_vars.items():
    #             value = var.get()
    #             if value == '': 
    #                 field = self.__FRAMES[key][-1].get('_text' if key in ('full_name', 'cover_type') else 'text')
    #                 raise Exception(f'Нет данных в поле: {field}')
    #             if key in numbered_var:
    #                 value = int(value) if value.isdigit() else 0
    #             yield value
    #     return self.product_type(*handler())    # type: ignore


    # def write_to_library(self) -> None:
    #     """Ф-я для обновления/записи информации библиотеку"""
    #     try:
    #         product = self.get_values_from_widgets()
    #         if self.module == 'change':
    #             AppManager.lib.change(product)
    #             title, message = 'Изменение продукта', f'Данне успешно обновлены для:\n{product.full_name}'
    #         else:
    #             AppManager.lib.add(product)
    #             title, message = 'Добавление  продукта', f'Продукт:\n{product.full_name}\nуспешно добавлен в библиотеку'
    #         tkmb.showinfo(title, message, parent=self)
    #     except Exception as e:
    #         tkmb.showwarning('Ошибка', str(e), parent=self)
