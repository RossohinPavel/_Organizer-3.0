from typing import Callable, Any, Iterator, Literal
from ...._appmanager import AppManager
from ..._source import *
from ....library.properties import Properties
from ....library.library import Product


class AssistWindow(ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    __window_size = {
        'Album': (498, 528), 
        'Canvas': (498, 278), 
        'Journal': (498, 278), 
        'Layflat': (498, 425),
        'Photobook': (498, 488), 
        'Photofolder': (498, 381), 
        'Subproduct': (498, 238)
        }

    __FRAMES = {
        'full_name': ('full_name', 'entry', 'left', {'_text': 'Полное имя продукта', 'width': 80}),
        'segment': ('options', 'radio', 'left', {'text': 'Сегмент продукции'}),
        'short_name': ('options', 'combo', 'left', {'text': 'Короткое имя'}),
        'product_format': ('options', 'combo', 'left', {'text': 'Формат продукта'}),
        'book_option': ('options', 'radio', 'right', {'text': 'Опция сборки книги'}),
        'lamination': ('options', 'radio', 'right', {'text': 'Ламинация'}),
        'cover_type': ('cover_type', 'radio', 'left',  {'_text': 'Тип сборки обложки'}),
        'carton_length': ('cover_val', 'entry', 'left', {'text': 'ДЛИННА картонки'}),
        'carton_height': ('cover_val',  'entry', 'left', {'text': 'ВЫСОТА картонки'}),
        'cover_flap': ('cover_val', 'combo', 'right', {'text': 'Значение КЛАПАНА обложки'}),
        'cover_joint': ('cover_val', 'combo', 'right', {'text': 'Значение ШАРНИРА обложки'}),
        'cover_print_mat': ('print_mat', 'combo', 'left', {'text': 'Печатный материал обложки'}),
        'page_print_mat': ('print_mat', 'combo', 'right', {'text': 'Печатный материал разворотов'}),
        'cover_canal': ('individual', 'combo', 'left', {'text': "'Канал' обложки"}),
        'page_canal': ('individual', 'combo', 'right', {'text': "'Канал' разворотов"}),
        'dc_top_indent': ('individual', 'entry', 'left', {'text': 'Отступ СВЕРХУ в мм'}),
        'dc_left_indent': ('individual', 'entry', 'left', {'text': 'Отступ СЛЕВА в мм'}),
        'dc_overlap': ('individual', 'entry', 'right', {'text': 'НАХЛЕСТ для переплета в мм'}),
        'dc_break': ('individual', 'check', 'right', {'text': 'Раскодировка с разрывом'})
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.module: Literal['add', 'copy', 'change'] = kwargs.pop('module')
        category, rus_name = kwargs.pop('category')
        product: str = kwargs.pop('product')
        self.width, self.height = self.__window_size[category]
        self.product_vars = {}  # Словарь для хранения переменных виджетов
        self.product_type = AppManager.lib.get_ptype(category)
        self.properties = Properties(category)
        super().__init__(*args, **kwargs)
        self.title({'add': 'Добавление', 'copy': 'Копирование', 'change': 'Изменение'}[self.module] + ' продукта: ' + rus_name)
        self.show_main_widgets()
        if self.module != 'add':
            self.insert_values_from_lib_to_widgets(product)
        self.show_buttons()

    def show_main_widgets(self) -> None:
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        # Определяем словарь для групп особенностей
        mf = {
            'full_name': self.show_m_frame(self.__FRAMES['full_name'][-1]['_text']),
            'options': self.show_m_frame('Общие особенности продукта'),
            'cover_type': self.show_m_frame(self.__FRAMES['cover_type'][-1]['_text']),
            'cover_val': self.show_m_frame('Технические размеры обложки'),
            'print_mat': self.show_m_frame('Печатный материал'),
            'individual': self.show_m_frame('Индивидуальные особенности продукта')
            }
        # Определяем словарь для функций для упрощения доступа
        funcs = {'entry': self.__show_entry, 'radio': self.__show_radio, 'combo': self.__show_combobox, 'check': self.__show_check}
        # Словарь для хранения информации для разделения виджетов по сторонам
        sides = {'left': [], 'right': []}
        # Непосредственно, отрисовка виджетов
        for frm in self.product_type._fields:
            m_name, child, side, kwargs = self.__FRAMES[frm]
            if not isinstance(mf[m_name], LabeledFrame):
                mf[m_name] = mf[m_name]()   #type: ignore
                sides['left'].clear() ; sides['right'].clear()
                sides['left'].extend({'row': i, 'column': 0} for i in range(3))
                sides['right'].extend({'row': i, 'column': 1} for i in range(3))
            kwargs.update({'padx': 1.48, **sides[side].pop(0)})
            funcs[child](frm, mf[m_name].container, **kwargs)

    def show_m_frame(self, text: str) -> Callable[[], LabeledFrame]:
        """Замыкание для отрисовки мастер-фреймов"""
        def wrapper() -> LabeledFrame:
            frame = LabeledFrame(master=self, text=text)
            frame.pack(expand=1, fill='x')
            return frame
        return wrapper

    def __show_entry(self, key: str, container: ttk.Frame, **kwargs: Any) -> None:
        """Конструктор фрейма для отрисовки Entry виджета"""
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = var = tk.StringVar(master=container)
        entry = ttk.Entry(master=frame, width=kwargs.get('width', 39), textvariable=var,
                          state='disabled' if key == 'full_name' and self.module == 'change' else 'normal')
        entry.pack()
        frame.grid(row=kwargs.get('row', 0), column=kwargs.get('column', 0), padx=kwargs.get('padx', 0))

    def __show_radio(self, key: str, container: ttk.Frame, **kwargs: Any) -> None:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        pos = [{'row': 1, 'column': i} for i in range(5)]
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).grid(row=0, column=0, columnspan=3, sticky='nw')
        values = self.properties(key)
        self.product_vars[key] = var = tk.StringVar(master=container, value=values[0])
        for name in values:
            ttk.Radiobutton(master=frame, text=name, value=name, variable=var).grid(**pos.pop(0), sticky='ew')  #type: ignore
        frame.grid(row=kwargs['row'], column=kwargs['column'], sticky='ew', padx=kwargs.get('padx', 0))

    def __show_combobox(self, key: str, container: ttk.Frame, **kwargs: Any) -> None:
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        frame = tk.Frame(master=container)
        if 'text' in kwargs:
            ttk.Label(master=frame, text=kwargs['text']).pack(anchor='nw')
        self.product_vars[key] = ttk.Combobox(master=frame, width=kwargs.get('width', 36), state='readonly', values=self.properties(key))
        self.product_vars[key].pack(anchor='nw', padx=0.5)
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def __show_check(self, key: str, container: ttk.Frame, **kwargs: Any) -> None:
        """Конструктор для отрисовки чек фреймов"""
        frame = tk.Frame(master=container)
        self.product_vars[key] = var = tk.IntVar(master=container)
        ttk.Checkbutton(master=frame, text=kwargs['text'], variable=var).pack()
        frame.grid(row=kwargs['row'], column=kwargs['column'], padx=kwargs.get('padx', 0))

    def show_buttons(self) -> None:
        """Функция для отрисовки кнопок"""
        frame = tk.Frame(self, height=28)
        MyButton(frame, text='Сохранить', width=30, command=self.write_to_library).place(x=130, y=0)
        MyButton(frame, text='Закрыть', width=10, command=self.destroy).place(x=415, y=0)
        frame.pack(expand=1, fill='x')

    def insert_values_from_lib_to_widgets(self, product_name: str) -> None:
        """Метод для вставки полученных значений из бд в виджеты"""
        product = AppManager.lib.get(product_name)
        for i, attr in enumerate(product._fields):      # type: ignore      # Продукт точно вернется
            if attr == 'full_name' and self.module == 'copy': continue
            self.product_vars[attr].set(product[i])     # type: ignore

    def get_values_from_widgets(self) -> Product:
        """Метод для получения информации из виджетов.\n
        Возвращает Product если все значения были заполнены,\n
        генерирует исключение в противном случае."""
        numbered_var = ('carton_length', 'carton_height', 'dc_top_indent', 'dc_left_indent', 'dc_overlap')
        def handler() -> Iterator[str | int]:
            for key, var in self.product_vars.items():
                value = var.get()
                if value == '': 
                    field = self.__FRAMES[key][-1].get('_text' if key in ('full_name', 'cover_type') else 'text')
                    raise Exception(f'Нет данных в поле: {field}')
                if key in numbered_var:
                    value = int(value) if value.isdigit() else 0
                yield value
        return self.product_type(*handler())    # type: ignore

    def write_to_library(self) -> None:
        """Ф-я для обновления/записи информации библиотеку"""
        try:
            product = self.get_values_from_widgets()
            if self.module == 'change':
                AppManager.lib.change(product)
                title, message = 'Изменение продукта', f'Данне успешно обновлены для:\n{product.full_name}'
            else:
                AppManager.lib.add(product)
                title, message = 'Добавление  продукта', f'Продукт:\n{product.full_name}\nуспешно добавлен в библиотеку'
            tkmb.showinfo(title, message, parent=self)
        except Exception as e:
            tkmb.showwarning('Ошибка', str(e), parent=self)
