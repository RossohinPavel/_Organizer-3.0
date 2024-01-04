from ...source import *
from ...source.images import IMAGES
from ...source.order_name_validate_entry import ONVEntry
# from ...orders_repr.proxy_file_handler import FileHandlerProxy


class HandlerWindow(ChildWindow):
    """Конструктор для окон обработчиков файлов"""
    # Геометрия окна
    width, height = 280, 194

    # Название окна и текстовая информация, используемая обработчиком
    win_title = 'Обработчик'
    handler_description = 'Описание того, что делает обработчик'
    handler_option_text = 'Опция обработчика'

    # Ссылка на объект - обработчик 
    file_handler = None

    def __init__(self):
        self.widget_dct = {}
        super().__init__()
        self.widget_dct['onve'].focus_set()
        self.bind('<Return>', self.run_handler)

    def main(self, **kwargs):
        self.show_info_label()
        self.show_order_name_validate_widgets()
        self.show_handler_option_widget()
        self.show_target_edition_widgets()
        self.show_miss_edition_widgets()
        self.show_buttons()
        self.bind('<KeyPress>', self.__enter_event)

    def __enter_event(self, event):
        """Событие, перемещающее фокус на энтри виджет, при нажатии кнопки"""
        entry = self.widget_dct['onve']
        if entry != self.focus_get():
            entry.focus_set()
            entry.event_generate('<KeyPress>', keysym=event.keysym)
        
    def show_info_label(self) -> None:
        """Отрисовка лейбла с информацией - подсказкой"""
        info = ttk.Label(master=self, image=IMAGES['question'])
        info.place(x=260, y=0)

    def show_order_name_validate_widgets(self) -> None:
        """Отрисовка виджета ввода имени заказа"""
        self.widget_dct['onve'] = onve = ONVEntry(self, _func=self.get_order)
        onve.pack(pady=(5, 0), padx=60, fill=ttkc.X)

        self.widget_dct['text_var'] = var = ttk.StringVar(master=self, value='test')
        ttk.Label(self, textvariable=var).pack(pady=(5, 0))
        
        ttk.Separator(self, orient='horizontal').pack(fill=ttkc.X, padx=5)

    def show_handler_option_widget(self) -> None:
        """Отрисовка виджета управления опциями обработчика"""
        self.widget_dct['handler_option'] = h_o = ttk.BooleanVar(master=self, value=True)

        chbtn = ttk.Checkbutton(self, text=self.handler_option_text, variable=h_o)
        chbtn.pack(anchor=ttkc.NW, padx=5, pady=5)

    def show_target_edition_widgets(self) -> None:
        """Отрисовка виджета тиражей, который будут обработаны"""
        self.widget_dct['target_combo'] = combo = ttk.Combobox(self, state='disabled', width=36)
        combo.pack(padx=5)

        combo.set('Целевые тиражи:') 
        combo.bind('<<ComboboxSelected>>', lambda _: combo.set('Целевые тиражи:'))

    def show_miss_edition_widgets(self) -> None:
        """Отрисовка виджета тиражей, которые будут пропущены обработчиком"""
        self.widget_dct['miss_combo'] = combo = ttk.Combobox(self, state='disabled', width=36)
        combo.pack(padx=5, pady=3)

        combo.set('Будут пропущенны:')
        combo.bind('<<ComboboxSelected>>', lambda _: combo.set('Будут пропущенны:'))

    def show_buttons(self) -> None:
        """Отрисовка кнопок"""
        start = ttk.Button(
            self, 
            style='minibtn.Outline.TButton',
            text='Запуск', 
            command=lambda: print(self.winfo_geometry())
            # command=self.run_handler
        )
        start.pack(pady=5, fill=ttkc.X, padx=60)

    def get_order(self, order_name):
        """Получение прокси объекта и выведение его элементов в виджете"""
        proxy = FileHandlerProxy(order_name, self.__predicate)
        if proxy is None:
            self.widget_dct['text_var'].set(f'Не могу найти заказ {order_name}')
            return
        self.reset_to_default()
        self.update_combo(proxy)

    def __predicate(self, product_obj) -> object | None:
        """
            Возвращает результат работы ф-ии handler_predicate 
            или None, если продукта нет в библиотеке
        """
        return self.handler_predicate(product_obj) if product_obj else None

    def handler_predicate(self, product_obj) -> object | None:
        """
            Возвращает продукт, если он соответсвует типу 
            обработчика. Иначе - возвращает None
        """
        raise Exception('Функция handler_predicate не переопределена в дочернем классе')

    def update_combo(self, proxy):
        """
            Обновление значений виджета целевых тиражей. 
            Так же записывает прокси объект в общий словарь.
        """
        target, miss = [], []
        for i in range(len(proxy.content)):
            target.append(proxy.content[i].name) if proxy.products[i] else miss.append(proxy.content[i].name)
        if target:
            self.widget_dct['text_var'].set(f'Обработка {proxy.name}')
            self.widget_dct['target_combo'].config(values=target, state='readonly')
            self.widget_dct['proxy'] = proxy
        else:
            self.widget_dct['text_var'].set(f'В заказе {proxy.name} нет целевых тиражей')
        if miss:
            self.widget_dct['miss_combo'].config(values=miss, state='readonly')

    def run_handler(self, event=None, **kwargs):
        """Функция запуска обработчика"""
        res = self.widget_dct.pop('proxy', None)
        if not res:
            tkmb.showwarning(parent=self, title=self.win_title, message='Не указан заказ или в заказе нет целевых тиражей.')
            return
        if self.file_handler is None:
            raise Exception('Файловый обработчик не переопределен в дочернем классе')
        kwargs['handler_option'] = self.widget_dct['handler_option'].get()
        self.storage.tm.create_task(self.file_handler, args=(res, ), kwargs=kwargs)
        tkmb.showinfo(parent=self, title=self.win_title, message=f'Заказ {res.name} поставлен в очередь обработки')
        self.reset_to_default()

    def reset_to_default(self):
        self.widget_dct['text_var'].set('')
        self.widget_dct['target_combo'].config(values=tuple(), state='disabled')
        self.widget_dct['miss_combo'].config(values=tuple(), state='disabled')
