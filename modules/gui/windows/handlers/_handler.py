from ..source import *
from ..frames.order_name_validate_frame import ONVFrame
from ...orders_repr.proxy_file_handler import FileHandlerProxy


class HandlerWindow(ChildWindow):
    """Конструктор для окон обработчиков файлов"""
    width = 277
    height = 153
    win_title = 'Обработчик'
    file_handler = None
    handler_description = 'Описание того, что делает обработчик'
    handler_option_text = 'Опция обработчика'

    def __init__(self, *args, **kwargs):
        self.widget_dct = {}
        super().__init__(*args, **kwargs)
        self.widget_dct['onvf']._entry.focus_set()
        self.bind('<Return>', self.run_handler)

    def main(self, *args, **kwargs):
        frame = LabeledFrame(master=self)
        frame.pack(expand=1, fill='both')
        self.show_info_label(frame)
        self.show_order_name_validate_widgets(frame.container)
        self.show_handler_option_widget(frame.container)
        self.show_target_edition_widgets(frame.container)
        self.show_miss_edition_widgets(frame.container)
        self.show_buttons(frame.container)
        self.bind('<KeyPress>', self.__enter_event)

    def __enter_event(self, event):
        entry = self.widget_dct['onvf']._entry
        if entry != self.focus_get():
            entry.focus_set()
            entry.event_generate('<KeyPress>', keysym=event.keysym)

    def show_info_label(self, frame):
        """Отрисовка лейбла с подсказкой о том, что делает обработчик"""
        info = ttk.Label(master=frame, image=self.master.question_ico)
        info.place(x=249, y=1)
        info.bind('<Button-1>', lambda event: TipWindow(self, mouse_event=event, text=self.handler_description))

    def show_order_name_validate_widgets(self, container):
        """Отрисовка виджета ввода имени заказа"""
        onvf = ONVFrame(master=container, func=self.get_order)
        onvf.pack(pady=(1, 0))
        self.widget_dct['onvf'] = onvf
        self.widget_dct['text_var'] = tk.StringVar(master=self)
        ttk.Label(master=container, textvariable=self.widget_dct['text_var']).pack()
        ttk.Frame(master=container, relief='solid').pack(fill='x')

    def show_handler_option_widget(self, container):
        """Отрисовка виджета управления опциями обработчика"""
        handler_option = tk.BooleanVar(master=self, value=True)
        self.widget_dct['handler_option'] = handler_option
        ttk.Checkbutton(master=container, text=self.handler_option_text, variable=handler_option).pack(anchor='nw')

    def show_target_edition_widgets(self, container):
        """Отрисовка виджета тиражей, который будут обработаны"""
        combo = ttk.Combobox(master=container, state='disabled', width=40)
        combo.set('Целевые тиражи:')
        combo.pack(padx=1)
        combo.bind('<<ComboboxSelected>>', lambda event: combo.set('Целевые тиражи:'))
        self.widget_dct['target_combo'] = combo

    def show_miss_edition_widgets(self, container):
        """Отрисовка виджета тиражей, которые будут пропущены обработчиком"""
        combo = ttk.Combobox(master=container, state='disabled', width=40)
        combo.set('Будут пропущенны:')
        combo.bind('<<ComboboxSelected>>', lambda event: combo.set('Будут пропущенны:'))
        combo.pack(padx=1, pady=3)
        self.widget_dct['miss_combo'] = combo

    def show_buttons(self, frame):
        """Отрисовка кнопок"""
        MyButton(master=frame, text='Запуск', command=self.run_handler, width=10).pack(side='left', padx=1, pady=(0, 1))
        MyButton(master=frame, text='Выход', command=self.destroy, width=10).pack(side='right', padx=1, pady=(0, 1))

    def get_order(self, order_name):
        """Получение прокси объекта и выведение его элементов в виджете"""
        proxy = FileHandlerProxy(order_name, self.__predicate)
        if proxy is None:
            self.widget_dct['text_var'].set(f'Не могу найти заказ {order_name}')
            return
        self.reset_to_default()
        self.update_combo(proxy)

    def __predicate(self, product_obj) -> object | None:
        """Возвращает результат работы ф-ии handler_predicate или None, если продукта нет в библиотеке"""
        return self.handler_predicate(product_obj) if product_obj else None

    def handler_predicate(self, product_obj) -> object | None:
        """Возвращает продукт, если он соответсвует типу обработчика. Иначе - возвращает None"""
        raise Exception('Функция handler_predicate не переопределена в дочернем классе')

    def update_combo(self, proxy):
        """Обновление значений виджета целевых тиражей. Так же записывает прокси объект в общий словарь"""
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