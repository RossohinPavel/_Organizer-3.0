from gui._source import *
from file_handlers import RoddomHandler
from appmanager import AppManager


class Roddom(ChildWindow):
    """Окно управления заказами роддома"""
    WIN_GEOMETRY = Geometry(280, 250)
    LIN_GEOMETRY = Geometry(315, 282)
    win_title='Роддом'
    
    def main(self, **kwargs) -> None:
        # Переменные, необходимые для работы
        self.order_obj = None

        default_text = 'Для подсчета количества\nотпечатков в заказе, нажмите на\nкнопку \'Посчитать заказ\' и\nвыберете нужный.'

        self.info_var = ttk.StringVar(master=self, value=default_text)
        self.txt_sum = ttk.BooleanVar(master=self, value=True)

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

        frame = ttk.LabelFrame(master=self, text='Папка, где хранятся заказы Роддом\'а')
        frame.pack(fill='x', padx=5, pady=(5, 0))

        upd_btn = ttk.Button(
            master=frame, 
            text=AppManager.stg.roddom_dir, 
            command=update_dir,
            style='l_jf.TButton'
            )
        upd_btn.pack(
            expand=1, 
            fill='x', 
            padx=5, 
            pady=(0, 5)
            )

    def show_info_widget(self) -> None:
        """Отрисовка виджета информации о заказе"""
        frame = ttk.LabelFrame(master=self, text='Информация', padding=(3, 0, 3, 3))
        frame.pack(expand=1, fill='both', padx=5, pady=(5, 0))
        ttk.Label(master=frame, textvariable=self.info_var, font='12').pack(anchor='w')

    def show_buttons(self):
        """Отрисовка виджетов кнопок"""
        chbtn = ttk.Checkbutton(
            self, 
            text='Сохранять результаты в sum.txt', 
            variable=self.txt_sum,
            style='success-round-toggle'
            )
        chbtn.pack(anchor='w', padx=5, pady=(5, 0))

        btn1 = ttk.Button(
            self, 
            text='Посчитать заказ', 
            width=18, 
            command=self.calc_order
            )
        btn1.pack(anchor='w', padx=5, pady=5)

        btn2 = ttk.Button(
            self, 
            text='Скопировать инфо', 
            width=18, 
            command=lambda: print(self.winfo_geometry())
            # command=self.info_to_clipboard
            )
        btn2.pack(side='left', padx=5, pady=(0, 5))

        btn3 = ttk.Button(
            self, 
            text='Отправить в печать', 
            width=18, 
            command=self.to_print
            )
        btn3.pack(side='right', padx=(0, 5), pady=(0, 5))

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
        tkmb.showinfo(
            parent=self, 
            title='Отправка в печать', 
            message=f'Заказ {self.order_obj.order} отправлен в печать'
            )

    def info_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.info_var.get())
