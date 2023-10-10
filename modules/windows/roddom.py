import modules.windows.source as source
from modules.windows.frames import LabeledFrame
from modules.file_handlers.roddom import Roddom


class RoddomWindow(source.ChildWindow):
    def do_before(self, *args, **kwargs):
        self.width = 253
        self.height = 216
        self.order_obj = None

    def do_after(self, *args, **kwargs):
        self.title('Роддом')
        self.show_directory_widget()
        self.info_var = source.tk.StringVar(master=self)
        self.show_info_widget()
        self.txt_sum = source.tk.BooleanVar(master=self, value=True)
        self.show_buttons()

    def show_directory_widget(self):
        """Отрисовка виджета отображения папки роддома и кнопки ее смены"""
        def update_dir():
            """Функция смены папки роддома"""
            path = source.tkfd.askdirectory()
            if path:
                self.app_m.stg.roddom_dir = path
                upd_btn.config(text=path)

        frame = LabeledFrame(master=self, text='Папка, где хранятся заказы Роддом\'а')
        frame.pack(fill='x')
        upd_btn = source.MyButton(master=frame.container, text=self.app_m.stg.roddom_dir, command=update_dir)
        upd_btn.pack(expand=1, fill='x')

    def show_info_widget(self):
        """Отрисовка виджета информации о заказе"""
        frame = LabeledFrame(master=self)
        frame.config(padding=(3, 0, 3, 3))
        frame.pack(expand=1, fill='both')
        label = source.ttk.Label(master=frame.container, textvariable=self.info_var, font=12)
        label.pack(anchor='w')

    def show_buttons(self):
        """Отрисовка виджетов кнопок"""
        text_res_cb = source.ttk.Checkbutton(self, text='Сохранять результаты в sum.txt', variable=self.txt_sum)
        text_res_cb.pack(anchor='w', padx=2)
        calc_btn = source.MyButton(self, text='Посчитать заказ', width=16, command=self.calc_order)
        calc_btn.pack(anchor='w', padx=3, pady=3)
        copy_inf_btn = source.MyButton(self, text='Скопировать инфо', width=16, command=self.info_to_clipboard)
        copy_inf_btn.pack(side='left', padx=3, pady=(0, 3))
        to_print_btn = source.MyButton(self, text='Отправить в печать', width=16, command=self.to_print)
        to_print_btn.pack(side='right', padx=(0, 3), pady=(0, 3))

    def calc_order(self):
        """Инициализация подсчета информации в заказе"""
        path = source.tkfd.askdirectory(parent=self, initialdir=self.app_m.stg.roddom_dir)
        if not path:
            return
        self.order_obj = Roddom(path, self.txt_sum.get())
        day = '-'.join(self.order_obj.order.split('-')[::-1])
        info = '\n'.join(f'{" "*5}{k}: {v}' for k, v in self.order_obj.get_calc_info().items())
        self.info_var.set(f'{day}\n{info}')

    def to_print(self):
        path = source.tkfd.askdirectory(parent=self, initialdir=self.app_m.stg.t_disc)
        if not path:
            return
        self.clipboard_clear()
        self.clipboard_append(f'{path}/{self.order_obj.order}\n\n{self.order_obj.order} -- Роддом')
        self.app_m.tm.create_task(self.order_obj.to_print, args=(path, ))

    def info_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get())
