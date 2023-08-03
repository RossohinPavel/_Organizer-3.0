import modules.windows.source as source


class SettingsWindow(source.ChildWindow):
    """Окно основных настроек приложения"""
    def main(self):
        self.title('Настройки')
        self.show_log_check_depth_widgets()
        self.show_log_widgets()
        self.show_directory_widgets()
        self.show_close_button()

    def show_separator(self, row=0):
        """Вспомогательная ф-я для отрисовки разделителя фреймов"""
        separator = source.tk.Frame(master=self, background='black', height=1)
        separator.grid(row=row, column=0, columnspan=2, sticky='EW', pady=1, padx=1)

    def show_log_check_depth_widgets(self, row=0):
        """Отрисовка виджетов для настройки глубины проверки лога"""
        r1 = 'Рекомендуемы значения для глубины проверки: 1 - 2 папки\n'
        r2 = 'При необходимости, захватит заказы с прошлого дня\n'
        r3 = 'Можно задать больше, но после первого\nсканирования рекомендуется вернуть значения по умолчанию.\n'
        r4 = 'В особенности, это актуально для автоматического режима.'

        def get_entry_value():
            value = entry_var.get()
            if value.isdigit():
                self.settings.log_check_depth = int(value)
                update_label()
            entry.delete(0, source.tk.END)

        def update_label(): label.config(text=f'Глубина проверки лога: {self.settings.log_check_depth} папок (дней)')

        label = source.ttk.Label(master=self)
        label.grid(row=row, column=0, columnspan=2, sticky='W')
        update_label()
        entry_var = source.tk.StringVar(master=self)
        entry = source.ttk.Entry(master=self, textvariable=entry_var)
        entry.grid(row=row+1, column=0, sticky='EW', padx=2)
        button = source.MyButton(master=self, text='Задать', command=get_entry_value)
        button.grid(row=row+1, column=1, sticky='EW', padx=1)
        info_label = source.ttk.Label(master=self, text=r1 + r2 + r3 + r4)
        info_label.grid(row=row+2, column=0, columnspan=2)
        self.show_separator(row=row+3)

    def show_log_widgets(self, row=4):
        """Сборная ф-я для отрисовки виджетов управления логом"""
        self.show_log_mode_widgets(row)
        self.show_separator(row+3)

    def show_log_mode_widgets(self, row):
        """Отрисовка виджетов управления режимом записи лога"""
        def check_autolog(): check_btn.config(state='normal' if self.settings.autolog else 'disabled')
        def select_cb(): self.settings.orders_complete_check = self.__dict__['check_complete'].get()

        def select_rb():
            self.settings.autolog = self.__dict__['log_mode'].get()
            check_autolog()

        label = source.ttk.Label(master=self, text='Режим записи лога')
        label.grid(row=row, column=0, sticky='W')
        self.__dict__['log_mode'] = source.tk.BooleanVar(master=self, value=self.settings.autolog)
        self.__dict__['check_complete'] = source.tk.BooleanVar(master=self, value=self.settings.orders_complete_check)
        radio1 = source.ttk.Radiobutton(master=self, text='Автоматический', command=select_rb,
                                        value=True, variable=self.__dict__['log_mode'])
        radio1.grid(row=row+1, column=0, sticky='W')
        radio2 = source.ttk.Radiobutton(master=self, text='Ручной', command=select_rb,
                                        value=False, variable=self.__dict__['log_mode'])
        radio2.grid(row=row+1, column=1, sticky='W')
        check_btn = source.ttk.Checkbutton(master=self, text='Проверка целостоности заказов', command=select_cb,
                                           variable=self.__dict__['check_complete'])
        check_btn.grid(row=row+2, column=0, sticky='W', columnspan=2)
        check_autolog()

    def show_directory_widgets(self, row=8):
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.show_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc', row, 0)
        self.show_directory_frame('Диск печати заказов \'О\'', 'o_disc', row, 1)
        self.show_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc', row+2, 0)

    def show_directory_frame(self, text, stg_attr, row, column):
        """Отрисовка виджетов управления рабочими папками"""
        def update_directory():
            path = source.tkfd.askdirectory(parent=self, initialdir=getattr(self.settings, stg_attr), title=f'Выберите: {text}')
            if path:
                setattr(self.settings, stg_attr, path)
                button.config(text=getattr(self.settings, stg_attr))

        label = source.ttk.Label(master=self, text=text)
        label.grid(row=row, column=column, sticky='W')
        button = source.MyButton(master=self, width=24, text=getattr(self.settings, stg_attr), command=update_directory)
        button.grid(row=row+1, column=column, padx=1, pady=1)

    def show_close_button(self, row=12):
        """Отрисовка кнопки закрытия"""
        button = source.MyButton(master=self, text='Закрыть', command=self.destroy)
        button.grid(row=row, column=1, padx=1, pady=1, sticky='EW')
