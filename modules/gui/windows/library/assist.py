from ...source import *
from .alias import AliasInterface
from ....mytyping import Literal, Type, Iterator, Categories, Callable


class AssistWindow(ChildWindow):
    """Конструктор вспомогательных окон библиотеки"""
    width = 405
    height = 400

    MARKS = {
        'main': 'Основное',
        'cover': 'Обложка',
        'print_mat': 'Печать',
        'individual': 'Индивидуально'
        }

    def __draw_checkbutton_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор для отрисовки чек фреймов"""
        # Переменная
        self._vars[key] = var = ttk.IntVar(master)

        # Виджет
        cb = ttk.Checkbutton(
            master, 
            text=text, 
            variable=var,
            style='success-round-toggle'
        )
        cb.pack(padx=(5, 0), pady=(5, 0), anchor=ttkc.W)

    def __draw_combobox_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор фрейма для отрисовки Комбобокс виджета"""
        # Рисуем название свойства
        ttk.Label(master, text=text).pack(anchor=ttkc.NW)

        # Рисуем Комбобокс
        self._vars[key] = combo = ttk.Combobox(
            master=master, 
            state='readonly', 
            values=self._properties(key),   #type: ignore
            cursor='hand2'
        )
        combo.pack(fill=ttkc.X, pady=(0, 5))

    def __draw_entry_widget(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор фрейма для отрисовки Entry виджета"""
        # Рисуем название свойства
        ttk.Label(master=master, text=text).pack(anchor=ttkc.NW)

        # Текстовая переменная
        self._vars[key] = var = ttk.StringVar(master)

        # Энтри виджет
        ttk.Entry(master=master, textvariable=var).pack(fill=ttkc.X, pady=(0, 5))

    def __draw_radio_widgets(self, master: ttk.Frame, key: str, text: str) -> None:
        """Конструктор для отрисовки Радио-баттон-фреймов"""
        # Рисуем название свойства
        ttk.Label(master, text=text).pack(anchor=ttkc.NW)

        # Получаем свойства и определяем текстовую переменную 
        values = self._properties(key)
        self._vars[key] = var = ttk.StringVar(master, value=values[0])  #type: ignore

        container = None

        # Рисуем Radiobutton'ы
        for i, name in enumerate(values):
            # Формируем контейнер для правильного размещения Radiobutton'ов
            if i % 3 == 0:
                container = ttk.Frame(master)
                container.pack(fill=ttkc.BOTH)

            ttk.Radiobutton(
                master=container, 
                text=name, 
                value=name, 
                variable=var
            ).pack(
                padx=(5, 10),
                pady=5, 
                anchor=ttkc.NW, 
                side=ttkc.LEFT
            )

    FRAMES = {
        'segment': (                        # Название свойства продукта
            'main',                         # Название категории (вкладки в Notebook), куда будет помещен виджет
             __draw_radio_widgets,          # Cсылка на функцию для отрисовки соответствующий фреймов
             'Сегмент продукции'            # Текст для label 
             ),
        'short_name': ('main', __draw_combobox_widget, 'Короткое имя'),
        'format': ('main', __draw_combobox_widget, 'Формат продукта'),
        'book_option': ('main', __draw_radio_widgets, 'Опция сборки книги'),
        'lamination': ('main', __draw_radio_widgets, 'Ламинация'),
        'cover_type': ('cover', __draw_radio_widgets, 'Тип сборки обложки'),
        'carton_length': ('cover', __draw_entry_widget, 'ДЛИННА картонки'),
        'carton_height': ('cover',  __draw_entry_widget, 'ВЫСОТА картонки'),
        'cover_flap': ('cover', __draw_combobox_widget, 'Значение КЛАПАНА обложки'),
        'cover_joint': ('cover', __draw_combobox_widget, 'Значение ШАРНИРА обложки'),
        'cover_print_mat': ('print_mat', __draw_combobox_widget, 'Печатный материал обложки'),
        'page_print_mat': ('print_mat', __draw_combobox_widget, 'Печатный материал разворотов'),
        'cover_canal': ('individual', __draw_combobox_widget, "'Канал' обложки"),
        'page_canal': ('individual', __draw_combobox_widget, "'Канал' разворотов"),
        'dc_top_indent': ('individual', __draw_entry_widget, 'Отступ СВЕРХУ в мм'),
        'dc_left_indent': ('individual', __draw_entry_widget, 'Отступ СЛЕВА в мм'),
        'dc_overlap': ('individual', __draw_entry_widget, 'НАХЛЕСТ для переплета в мм'),
        'dc_break': ('individual', __draw_checkbutton_widget, 'Раскодировка с разрывом')
        }

    def __init__(self, master: Any, category: Type[Categories], id: int) -> None:
        # Сохраняем значения в объекте
        self._id = id
        self._category = category
        self._properties = AppManager.lib.properties(category.__name__)
        self._vars = {}
        self._alias: AliasInterface = None  #type: ignore
        self._update_func = master.redraw

        # Вызываем базовый класс
        super().__init__(master)

    def main(self, **kwargs) -> None:
        # Рисуем Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=1, padx=5, pady=5)

        # 1 вкладка для отрисовки фрейма названия и псевдонимов
        names = ttk.Frame(nb, padding=5)
        nb.add(names, text='Название')
        self.__draw_entry_widget(names, 'name', 'Введите название продукта')
        self._alias = AliasInterface(names)

        # Отрисовка остальных фреймов на основе атрибутов категории продукта
        self.draw_main_widgets(nb)

        # Наполняем значениями
        self.insert_values_from_lib_to_widgets()

        # Кнопка сохранить
        ttk.Button(
            self, 
            text='Сохранить', 
            width=14, 
            command=self.write_to_library
        ).pack(pady=(0, 5))


    def set_title(self, mode: str) -> None:
        """Установка заголовка окна"""
        match mode:
            case 'add': title = 'Добавление'
            case 'copy': title = 'Копирование'
            case 'change' | _ : title = 'Изменение'
        self.title(title + ' продукта: ' + self._category.__doc__)  #type: ignore

    def draw_main_widgets(self, notebook: ttk.Notebook) -> None:
        """Отображает менюшки на self.product_menus_frame согласно выбранному продукту"""
        # Переменная для хранения имени вкладки. 
        mark_name = None

        # Переменная для хранения фреймов, на которых будут отрисовываться виджеты
        mark = None

        # Непосредственно, отрисовка виджетов
        for field in self._category._fields[1:]:

            # Получаем настройки виджета из словаря
            w_mark_name, draw_func, text = self.FRAMES[field] #type: ignore

            # Инициализируем закладку, если ее нет.
            if mark_name != w_mark_name:
                mark_name = w_mark_name
                mark = ttk.Frame(notebook, padding=5)
                notebook.add(mark, text=self.MARKS[w_mark_name])

            # Отрисовываем связанные виджеты 
            draw_func(self, mark, field, text)

    def insert_values_from_lib_to_widgets(self) -> None:
        """Метод для вставки полученных значений из бд в виджеты"""
        # Получаем продукт из библиотеки и размещаем значения
        product = AppManager.lib.from_id(self._category, self._id)

        # Изменение название окна
        self.title(f'Редактирование {product.name}')

        for i, attr in enumerate(product._fields):
            self._vars[attr].set(product[i])    

        # Получаем псевдонимы продукта
        aliases = AppManager.lib.get_aliases(self._category, self._id)
        self._alias.insert(*(x[0] for x in aliases))

    def get_values_from_widgets(self) -> Categories:
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
                    field = self.FRAMES.get(key, '"__"')[-2] if key != 'name' else 'Полное имя'
                    raise Exception(f'Нет данных в поле: {field}')

                # Переводим в int целочисленные значения
                if key in numbered_var: value = int(value) if value.isdigit() else 0

                yield value

        # Пакуем и возвращаем кортеж
        return self._category(*_handler())  #type: ignore

    def write_to_library(self) -> None:
        """Ф-я для обновления/записи информации библиотеку"""
        # Обработчик исключений, чтобы прервать логику выполнения в случае ошибки
        try:
            # Получаем продукт и псевдонимы
            product = self.get_values_from_widgets()
            aliases = self._alias.get()

            # Обновляем продукт
            AppManager.lib.change(self._id, product, aliases)

            # Обновляем виджеты в основном окне
            self._update_func()

            # Вывод сообщения об успехе операции
            tkmb.showinfo('Редактирование', f'Данные обновлены для:\n{product.name}', parent=self)
        
        # Вывод сообщения об ошибке
        except Exception as e: 
            tkmb.showwarning('Ошибка', str(e), parent=self)
