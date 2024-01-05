from ..source import *
from ...file_handlers.roddom import RoddomHandler


class Roddom(ChildWindow):
    """Окно управления заказами роддома"""
    width = 314
    height = 228
    win_title='Роддом'
    
    def main(self, **kwargs) -> None:
        # Переменные, необходимые для работы
        self.order_obj = None

        self.show_directory_widget()

        default_text = 'Для подсчета количества\nотпечатков в заказе, нажмите на\nкнопку \'Посчитать заказ\' и\nвыберете нужную папку.'
        self.info_var = ttk.StringVar(master=self, value=default_text)
        self.txt_sum = ttk.BooleanVar(master=self, value=True)
        self.show_info_widget()

        self.show_buttons()

    def show_directory_widget(self) -> None:
        """Отрисовка виджета отображения папки роддома и кнопки ее смены"""
        def update_dir() -> None:
            """Функция смены папки роддома"""
            path = tkfd.askdirectory()
            if path:
                AppManager.stg.roddom_dir = path
                upd_btn.configure(text=path)
            
        HeaderLabel(self, text='Папка с заказами Роддом\'а').pack(fill=ttkc.X, padx=5, pady=(5, 2))

        upd_btn = ttk.Button(
            master=self, 
            style='l_jf.Outline.TButton', 
            command=update_dir,
            text=AppManager.stg.roddom_dir
            )
        upd_btn.pack(fill=ttkc.X, padx=10)

    def show_info_widget(self) -> None:
        """Отрисовка виджета информации о заказе"""
        container = ttk.Frame(self, height=115)
        container.pack(fill=ttkc.X, padx=5)

        lbl = ttk.Label(container, textvariable=self.info_var, font='TkDefaultFont 11')
        lbl.place(x=10, y=25)

        HeaderLabel(container, text='Информация').place(x=0, y=10, relwidth=1)

        info = ttk.Button(
            container,
            style='Libcopy.success.Outline.TButton',
            text='  i  ',
            command=self.info_to_clipboard
        )
        info.place(y=5, relx=0.91)

    def show_buttons(self):
        """Отрисовка виджетов кнопок"""
        chbtn = ttk.Checkbutton(
            self, 
            text='Сохранять результаты в sum.txt', 
            variable=self.txt_sum,
            style='success-round-toggle'
            )
        chbtn.pack(anchor=ttkc.W, padx=5, pady=5)

        container = ttk.Frame(self, padding=5)
        container.pack(fill=ttkc.X)

        btn1 = ttk.Button(
            container, 
            width=20,
            style='minibtn.Outline.TButton',
            text='Посчитать заказ', 
            command=self.calc_order
            )
        btn1.pack(padx=(0, 3), fill=ttkc.X, side=ttkc.LEFT)

        btn2 = ttk.Button(
            container, 
            width=20,
            style='minibtn.Outline.TButton',
            text='Отправить в печать', 
            command=self.to_print
            )
        btn2.pack(padx=(3, 0), fill=ttkc.X, side=ttkc.RIGHT)

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
