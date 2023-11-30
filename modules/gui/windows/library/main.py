from ..._source import *
from .assist import AssistWindow


class LibraryWindow(ChildWindow):
    """Окно управления библиотекой"""
    WIN_GEOMETRY = Geometry(450, 500)
    LIN_GEOMETRY = Geometry(450, 500)
    win_title = 'Библиотека'

    def __init__(self, /, **kwargs) -> None:
        super().__init__(AppManager.mw, **kwargs)

        # Основной фрейм с прокруткой
        scroled_frame = ScrolledFrame(self, bootstyle='round')
        scroled_frame.pack(fill='both', expand=1)

        # Растягиваем 1 столбик
        scroled_frame.columnconfigure(0, weight=1)

        # Установка новых виджетов
        for row, category in enumerate(AppManager.lib.headers):
            CollapsingInterface(row * 100, scroled_frame, category)


class LibMenubutton(tb.Menubutton):
    """Menubutton для представления продукта в библиотеке"""
    def __init__(self, colapsing_int: Any, text:str):
        self._interface = colapsing_int
        self._pname = text
        super().__init__(
            master=colapsing_int._lib_frame, 
            text=text, 
            style='ms.info.Outline.TMenubutton', 
            cursor='hand2'
            )
        self.show_menu()
    
    def delete_products(self):
        """Удаление продукта из библиотеки"""
        AppManager.lib.delete(self._interface._category.__name__, self._pname)
        self._interface.update_widgets()
    
    def show_info_box(self) -> None:
        product = AppManager.lib.get(self._pname)
        text = '\n'.join(f'{field} -- {getattr(product, field)}' for field in product._fields if field != 'full_name')
        tkmb.showinfo(parent=self.master.master.master, title=product.full_name, message=text)  #type: ignore

    def show_menu(self) -> None:
        """Отрисовка меню"""
        menu = tb.Menu(self)

        menu.add_command(
            label='Информация', 
            command=self.show_info_box
            )
        menu.add_command(
            label='Изменить', 
            command=lambda: AssistWindow(
                self._interface._lib_frame.master.master, # type: ignore
                mode='change',
                category=self._interface._category,
                product=self._pname,
                update_func=self._interface.update_widgets
                )
            )
        menu.add_command(
            label='Копировать',
            command=lambda: AssistWindow(
                self._interface._lib_frame.master.master, # type: ignore
                mode='copy',
                category=self._interface._category,
                product=self._pname,
                update_func=self._interface.update_widgets
                )
            )
        menu.add_command(label='Удалить', command=self.delete_products)
        self['menu'] = menu


class CollapsingInterface:
    """Интерфейс для управления отрисовкой дочерних виджетов"""
    __slots__ = '_row', '_lib_frame', '_category', '_container', '_state', '_btn1'

    def __init__(self, row: int, lib_frame: ScrolledFrame, category: Type[AppManager.lib.products]) -> None:
        # Сохраняем атрибуты
        self._row = row
        self._lib_frame = lib_frame
        self._category = category

        # Основная кнопка С заголовком продукта и функцией свертываня / развертывания
        self._btn1 = tb.Button(
            self._lib_frame,
            text='⌄  ' + self._category.__doc__, #type: ignore
            style='library.TButton', 
            command=self._toggle_open_close
            )
        self._btn1.grid(row=self._row, column=0, sticky='ew')

        # Вторая кнопка - добавление продукта в библиотеку
        tb.Button(
            self._lib_frame, 
            text='+' , 
            style='LibraryPlus.TButton',
            cursor='hand2',
            command=self.add_product
            ).grid(
                row=self._row, 
                column=1, 
                sticky='nsew', 
                padx=(0, 12)
                )
        
        # Положение виджета для устранения проверки. False - закрыт, True - открыт
        self._state = True

        # контейнер для виджетов
        self._container = ()
        self._update_container()
    
    def add_product(self):
        """Добавление продукта в библиотеку"""
        AssistWindow(
            master=self._lib_frame.master.master, # type: ignore
            mode='add',
            category=self._category,
            update_func=self.update_widgets
            )

    def _update_container(self) -> None:
        """Получение кнопок по продуктам из библиотеки"""
        def _func() -> Iterator[LibMenubutton]:
            """Внутренний генератор для получения кнопок"""
            for i, product in enumerate(sorted(AppManager.lib.headers[self._category]), 1):
                btn = LibMenubutton(self, text=product)
                btn.grid(
                    row=self._row + i, 
                    column=0, 
                    columnspan=2, 
                    sticky='ew',
                    padx=(5, 17),
                    pady=(0 if i != 1 else 5, 5)
                )
                
                yield btn
        
        # Обновляем контейнер и сворачиваем общий фрейм
        self._container = tuple(_func())
        self._toggle_open_close()
 
    def _toggle_open_close(self):
        """Открытие и закрытие виджета"""
        if self._state:
            for btn in self._container: btn.grid_remove()
            self._btn1.configure(text='⌄  ' + self._category.__doc__) #type: ignore
        else:
            for btn in self._container: btn.grid()
            self._btn1.configure(text='⌃  ' + self._category.__doc__) #type: ignore
        self._state = not self._state

    def update_widgets(self):
        """Обновление виджета актуальными продуктами"""
        # Уничтожаем все виджеты в контейнере
        for widget in self._container: widget.destroy()

        # Получаем актуальное состояние раскрытия
        current_state = self._state

        # Возвращаем раскрытие к начальному состоянию
        self._state = True

        # Обновляем контейнер виджетов
        self._update_container()

        # Если виджет был открыт на момент вызова метода, то открываем его снова
        if current_state: self._toggle_open_close()
