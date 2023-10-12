from .source import *
from .frames.order_name_validate_frame import ONVFrame


__all__ = ['CoverMarker']


class HandlerWindow(ChildWindow):
    """Конструктор для окон обработчиков файлов"""
    width = 277
    height = 153
    win_title = 'Обработчик'
    handler_description = 'Описание того, что делает обработчик'
    handler_option_text = 'Опция обработчика'

    def __init__(self, *args, **kwargs):
        self.widget_dct = {}
        super().__init__(*args, **kwargs)
        self.widget_dct['onvf']._entry.focus_set()

    def main(self, *args, **kwargs):
        frame = LabeledFrame(master=self)
        frame.pack(expand=1, fill='both')
        self.show_info_label(frame)
        self.show_order_name_validate_widgets(frame.container)
        self.show_handler_option_widget(frame.container)
        self.show_target_edition_widgets(frame.container)
        self.show_miss_edition_widgets(frame.container)
        self.show_buttons(frame.container)

    def show_info_label(self, frame):
        """Отрисовка лейбла с подсказкой о том, что делает обработчик"""
        info = ttk.Label(master=frame, image=self.master.BTN_ICO)
        info.place(x=249, y=1)
        info.bind('<Button-1>', lambda event: TipWindow(self, mouse_event=event, text=self.handler_description))

    def show_order_name_validate_widgets(self, container):
        """Отрисовка виджета ввода имени заказа"""
        onvf = ONVFrame(master=container)
        onvf.pack(pady=(1, 0))
        self.widget_dct['onvf'] = onvf
        ttk.Label(master=container, text='Нашел/не нашел заказ').pack()
        ttk.Frame(master=container, relief='solid').pack(fill='x')

    def show_handler_option_widget(self, container):
        """Отрисовка виджета управления опциями обработчика"""
        handler_option = tk.BooleanVar(master=self, value=True)
        self.widget_dct['handler_option'] = handler_option
        ttk.Checkbutton(master=container, text=self.handler_option_text, variable=handler_option).pack(anchor='nw')

    def show_target_edition_widgets(self, container):
        """Отрисовка виджета тиражей, который будут обработаны"""
        combo = ttk.Combobox(master=container, state='readonly', width=40)
        combo.pack(padx=1)
        self.widget_dct['target_combo'] = combo

    def show_miss_edition_widgets(self, container):
        """Отрисовка виджета тиражей, которые будут пропущены обработчиком"""
        combo = ttk.Combobox(master=container, state='readonly', width=40)
        combo.pack(padx=1, pady=3)
        self.widget_dct['miss_combo'] = combo

    def show_buttons(self, frame):
        """Отрисовка кнопок"""
        MyButton(master=frame, text='Запуск', command=lambda: print(self.geometry()), width=10).pack(side='left', padx=1, pady=(0, 1))
        MyButton(master=frame, text='Выход', command=self.destroy, width=10).pack(side='right', padx=1, pady=(0, 1))


class CoverMarker(HandlerWindow):
    """Разметка обложки"""
    win_title = 'Разметка обложки'
    handler_description = 'Разметка обратной стороны для обложкек.\nВ заказе будут обработаны все определившиеся ' \
                          'тиражи\nсогласно спецификации продукта. Для индивидуальных\nобложек файлы с сетками ' \
                          'будут сохранены в папке\nCovers, для одинаковых - Constant. При выборе опции\nобработки ' \
                          '\'Добавление бэкпринта\' на заднюю часть\nобложки будет нанесена информация о названии\n' \
                          'тиража и особенностях сборки продукта.'
    handler_option_text = 'Добавление бэкпринта'
