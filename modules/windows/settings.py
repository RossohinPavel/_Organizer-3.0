import modules.windows.source as source


class SettingsWindow(source.ChildWindow):
    """Окно основных настроек приложения"""
    def main(self):
        self.title('Настройки')
        self.show_log_check_depth_widgets()
        self.show_mode_widgets()
        self.show_directory_widgets()
        self.show_close_button()

    def show_separator(self, row=0):
        """Вспомогательная ф-я для отрисовки разделителя фреймов"""
        source.tk.Frame(master=self, bg='black', height=1).grid(row=row, column=0, columnspan=2, sticky='EW', pady=1, padx=1)

    def show_log_check_depth_widgets(self, row=0):
        """Отрисовка виджетов для настройки глубины проверки лога"""
        msg = ('Рекомендуемый глубина ~ 100 заказов.', 'Ограничено свободным объемом ОЗУ.')

        def get_entry_value():
            value = entry_var.get()
            if value.isdigit():
                self.app_m.Settings.log_check_depth = int(value)
                update_label()
            entry.delete(0, source.tk.END)

        def update_label():
            label.config(text=f'Глубина проверки лога: {self.app_m.Settings.log_check_depth} заказов (папок)')

        label = source.ttk.Label(master=self)
        label.grid(row=row, column=0, columnspan=2, sticky='W')
        update_label()
        entry_var = source.tk.StringVar(master=self)
        entry = source.ttk.Entry(master=self, textvariable=entry_var)
        entry.grid(row=row+1, column=0, sticky='EW', padx=2)
        button = source.MyButton(master=self, text='Задать', command=get_entry_value)
        button.grid(row=row+1, column=1, sticky='EW', padx=1)
        info_label = source.ttk.Label(master=self, text='\n'.join(msg))
        info_label.grid(row=row+2, column=0, columnspan=2, sticky='W')
        self.show_separator(row=row+3)

    def show_mode_widgets(self, row=4):
        """Сборная ф-я для отрисовки виджетов управления режимов работы программы"""
        def select_cb(var_name):
            setattr(self.app_m.Settings, var_name, self.__dict__[var_name].get())
            source.tkmb.showinfo(parent=self, title="Изменение настроек",
                                 message="Для вступления настроек в силу нужно перезагрузить программу")

        source.ttk.Label(master=self, text='Режимы работы программы').grid(row=row, column=0, sticky='W')
        self.__dict__['autolog'] = source.tk.BooleanVar(master=self, value=self.app_m.Settings.autolog)
        chbtn1 = source.ttk.Checkbutton(master=self, text='Автоматическое слежение за заказами',
                                        variable=self.__dict__['autolog'], command=lambda: select_cb('autolog'))
        chbtn1.grid(row=row + 1, column=0, sticky='W', columnspan=2)
        self.__dict__['autofile'] = source.tk.BooleanVar(master=self, value=self.app_m.Settings.autofile)
        chbtn2 = source.ttk.Checkbutton(master=self, text='Автоматическое копирование на диск О',
                                        variable=self.__dict__['autofile'], command=lambda: select_cb('autofile'))
        chbtn2.grid(row=row + 2, column=0, sticky='W', columnspan=2)
        self.show_separator(row+3)

    def show_directory_widgets(self, row=8):
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        self.show_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc', row, 0)
        self.show_directory_frame('Диск печати заказов \'О\'', 'o_disc', row, 1)
        self.show_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc', row+2, 0)

    def show_directory_frame(self, text, stg_attr, row, column):
        """Отрисовка виджетов управления рабочими папками"""
        def update_dir():
            path = source.tkfd.askdirectory(parent=self, initialdir=getattr(self.app_m.Settings, stg_attr),
                                            title=f'Выберите: {text}')
            if path:
                setattr(self.app_m.Settings, stg_attr, path)
                button.config(text=getattr(self.app_m.Settings, stg_attr))

        label = source.ttk.Label(master=self, text=text)
        label.grid(row=row, column=column, sticky='W')
        button = source.MyButton(master=self, width=24, text=getattr(self.app_m.Settings, stg_attr), command=update_dir)
        button.grid(row=row+1, column=column, padx=1, pady=1)

    def show_close_button(self, row=12):
        """Отрисовка кнопки закрытия"""
        source.MyButton(master=self, text='Закрыть', command=self.destroy).grid(row=row, column=1, padx=1, pady=1, sticky='EW')
