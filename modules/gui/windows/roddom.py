from gui._source import *
from file_handlers import RoddomHandler
from appmanager import AppManager


class Roddom(ChildWindow):
    """Окно управления заказами роддома"""
    width = 253
    height = 216

    def main(self, *args, **kwargs) -> None:
        self.order_obj = None
        self.title('Роддом')
        self.info_var = tk.StringVar(master=self)
        self.txt_sum = tk.BooleanVar(master=self, value=True)
        self.show_directory_widget()
        self.show_info_widget()
        self.show_buttons()

    def show_directory_widget(self) -> None:
        """Отрисовка виджета отображения папки роддома и кнопки ее смены"""
        def update_dir() -> None:
            """Функция смены папки роддома"""
            path = tkfd.askdirectory()
            if path:
                AppManager.stg.roddom_dir = path
                upd_btn.config(text=path)

        frame = LabeledFrame(master=self, text='Папка, где хранятся заказы Роддом\'а')
        frame.pack(fill='x')
        upd_btn = MyButton(master=frame.container, text=AppManager.stg.roddom_dir, command=update_dir)
        upd_btn.pack(expand=1, fill='x')

    def show_info_widget(self) -> None:
        """Отрисовка виджета информации о заказе"""
        frame = LabeledFrame(master=self)
        frame.config(padding=(3, 0, 3, 3))
        frame.pack(expand=1, fill='both')
        ttk.Label(master=frame.container, textvariable=self.info_var, font='12').pack(anchor='w')

    def show_buttons(self):
        """Отрисовка виджетов кнопок"""
        ttk.Checkbutton(self, text='Сохранять результаты в sum.txt', variable=self.txt_sum).pack(anchor='w', padx=2)
        MyButton(self, text='Посчитать заказ', width=16, command=self.calc_order).pack(anchor='w', padx=3, pady=3)
        MyButton(self, text='Скопировать инфо', width=16, command=self.info_to_clipboard).pack(side='left', padx=3, pady=(0, 3))
        MyButton(self, text='Отправить в печать', width=16, command=self.to_print).pack(side='right', padx=(0, 3), pady=(0, 3))

    def calc_order(self):
        """Инициализация подсчета информации в заказе"""
        path = tkfd.askdirectory(parent=self, initialdir=AppManager.stg.roddom_dir)
        if not path:
            return
        self.order_obj = RoddomHandler(path, self.txt_sum.get())
        day = '-'.join(self.order_obj.order.split('-')[::-1])
        info = '\n'.join(f'{" "*5}{k}: {v}' for k, v in self.order_obj.get_calc_info().items())
        self.info_var.set(f'{day}\n{info}')

    def to_print(self):
        if self.order_obj is None:
            tkmb.showwarning(parent=self, title='Отправка в печать', message='Заказ не выбран')
            return
        path = tkfd.askdirectory(parent=self, initialdir=AppManager.stg.t_disc)
        if not path:
            return
        self.clipboard_clear()
        self.clipboard_append(f'{path}/{self.order_obj.order}\n\n{self.order_obj.order} -- Роддом')
        AppManager.tm.create_task(self.order_obj.to_print, path)
        tkmb.showinfo(parent=self, title='Отправка в печать', message=f'Заказ {self.order_obj.order} отправлен в печать')

    def info_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get())
