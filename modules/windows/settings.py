import modules.windows.source as source


class SettingsWindow(source.ChildWindow):
    """Окно основных настроек приложения"""
    def main(self):
        self.title('Настройки')
        self.show_log_check_depth_widgets()
        self.show_mode_widgets()
        self.show_directory_widgets()
        source.MyButton(master=self, text='Закрыть', command=self.destroy, width=23).pack(anchor='se', pady=(2, 4), padx=4)

    def show_log_check_depth_widgets(self):
        """Отрисовка виджетов для настройки глубины проверки лога"""
        msg = ('Рекомендуемая глубина ~ 100 заказов.', 'Ограничено свободным объемом ОЗУ.')

        def get_entry_value():
            value = entry_var.get()
            if value.isdigit():
                self.app_m.Settings.log_check_depth = int(value)
                update_label()
            entry.delete(0, source.tk.END)

        def update_label():
            label.config(text=f'Текущее значение: {self.app_m.Settings.log_check_depth} заказов (папок)')

        frame = source.LabeledFrame(master=self, text='Глубина проверки лога')
        label = source.ttk.Label(master=frame.container)
        update_label()
        entry_var = source.tk.StringVar(master=self)
        entry = source.ttk.Entry(master=frame.container, textvariable=entry_var, width=26)
        btn = source.MyButton(master=frame.container, text='Задать', command=get_entry_value)
        info = source.ttk.Label(master=frame.container, text='\n'.join(msg))
        label.pack(side='top', anchor='nw')
        info.pack(side='bottom', anchor='nw')
        entry.pack(side='left', padx=(2, 4), pady=3)
        btn.pack(side='right', expand=1, fill='x')
        frame.pack(fill='x')

    def show_mode_widgets(self):
        """Сборная ф-я для отрисовки виджетов управления режимов работы программы"""
        def select_cb(var_name):
            setattr(self.app_m.Settings, var_name, self.__dict__[var_name].get())
            source.tkmb.showinfo(parent=self, title="Изменение настроек",
                                 message="Для вступления настроек в силу нужно перезагрузить программу")

        frame = source.LabeledFrame(master=self, text='Режимы работы программы')
        frame.pack(fill='x')
        self.__dict__['autolog'] = source.tk.BooleanVar(master=self, value=self.app_m.Settings.autolog)
        chbtn1 = source.ttk.Checkbutton(master=frame.container, text='Автоматическое слежение за заказами',
                                        variable=self.__dict__['autolog'], command=lambda: select_cb('autolog'))
        chbtn1.pack(anchor='nw')
        self.__dict__['autofile'] = source.tk.BooleanVar(master=self, value=self.app_m.Settings.autofile)
        chbtn2 = source.ttk.Checkbutton(master=frame.container, text='Автоматическое копирование на диск О',
                                        variable=self.__dict__['autofile'], command=lambda: select_cb('autofile'))
        chbtn2.pack(anchor='nw')

    def show_directory_widgets(self):
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        frame = source.LabeledFrame(master=self, text='Рабочие директории')
        frame.pack()
        self.show_directory_frame(frame.container, 'bottom', 'Диск операторов фотопечати \'Т\'', 't_disc', (1, 2))
        self.show_directory_frame(frame.container, 'left', 'Диск загрузки заказов \'Z\'', 'z_disc', (1, 1))
        self.show_directory_frame(frame.container, 'right', 'Диск печати заказов \'О\'', 'o_disc', (2, 1))

    def show_directory_frame(self, container, side, text, stg_attr, btn_pdx):
        """Отрисовка виджетов управления рабочими папками"""
        def update_dir():
            path = source.tkfd.askdirectory(parent=self, initialdir=getattr(self.app_m.Settings, stg_attr),
                                            title=f'Выберите: {text}')
            if path:
                setattr(self.app_m.Settings, stg_attr, path)
                btn.config(text=getattr(self.app_m.Settings, stg_attr))

        top_frame = source.ttk.Frame(master=container)
        top_frame.pack(side=side, anchor='nw')

        source.ttk.Label(master=top_frame, text=text).pack(anchor='nw')
        btn = source.MyButton(master=top_frame, width=22, text=getattr(self.app_m.Settings, stg_attr), command=update_dir)
        btn.pack(anchor='nw', padx=btn_pdx, pady=(0, 1))
