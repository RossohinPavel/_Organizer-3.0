from .._source import *
from typing import Literal
from ..._appmanager import AppManager


__all__ = ('SettingsWindow', )


class SettingsWindow(ChildWindow):
    """Окно основных настроек приложения"""
    width = 345
    height = 288

    def main(self, *args, **kwargs) -> None:
        self.title('Настройки')
        self.show_log_check_depth_widgets()
        self.show_mode_widgets()
        self.show_directory_widgets()
        MyButton(master=self, text='Закрыть', command=self.destroy, width=23).pack(anchor='se', pady=(2, 4), padx=4)

    def show_log_check_depth_widgets(self) -> None:
        """Отрисовка виджетов для настройки глубины проверки лога"""
        msg = ('Рекомендуемая глубина ~ 100 заказов.', 'Ограничено свободным объемом ОЗУ.')

        def get_entry_value() -> None:
            value = entry_var.get()
            if value.isdigit():
                AppManager.stg.log_check_depth = int(value)
                update_label()
            entry.delete(0, tk.END)

        def update_label() -> None:
            label.config(text=f'Текущее значение: {AppManager.stg.log_check_depth} заказов (папок)')

        frame = LabeledFrame(master=self, text='Глубина проверки лога')
        label = ttk.Label(master=frame.container)
        update_label()
        entry_var = tk.StringVar(master=self)
        entry = ttk.Entry(master=frame.container, textvariable=entry_var, width=26)
        btn = MyButton(master=frame.container, text='Задать', command=get_entry_value)
        info = ttk.Label(master=frame.container, text='\n'.join(msg))
        label.pack(side='top', anchor='nw')
        info.pack(side='bottom', anchor='nw')
        entry.pack(side='left', padx=(1, 4), pady=3)
        btn.pack(side='right', expand=1, fill='x', padx=(0, 1))
        frame.pack(fill='x')

    def show_mode_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления режимов работы программы"""
        def select_cb(var_name: str) -> None:
            setattr(AppManager.stg, var_name, self.__dict__[var_name].get())

        frame = LabeledFrame(master=self, text='Режимы работы программы')
        frame.pack(fill='x')
        self.__dict__['autolog'] = tk.BooleanVar(master=self, value=AppManager.stg.autolog)
        chbtn1 = ttk.Checkbutton(master=frame.container, text='Автоматическое слежение за заказами',
                                 variable=self.__dict__['autolog'], command=lambda: select_cb('autolog'))
        chbtn1.pack(anchor='nw')

    def show_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        frame = LabeledFrame(master=self, text='Рабочие директории')
        frame.pack()
        self.show_directory_frame(frame.container, 'bottom', 'Диск операторов фотопечати \'Т\'', 't_disc', (1, 2))
        self.show_directory_frame(frame.container, 'left', 'Диск загрузки заказов \'Z\'', 'z_disc', (1, 1))
        self.show_directory_frame(frame.container, 'right', 'Диск печати заказов \'О\'', 'o_disc', (2, 1))

    def show_directory_frame(self, container: ttk.Frame, side: Literal['left', 'right', 'top', 'bottom'], 
                             text: str, stg_attr: str, btn_pdx: tuple[int, int]) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        def update_dir() -> None:
            path = tkfd.askdirectory(parent=self, initialdir=getattr(AppManager.stg, stg_attr), title=f'Выберите: {text}')
            if path:
                setattr(AppManager.stg, stg_attr, path)
                btn.config(text=getattr(AppManager.stg, stg_attr))

        top_frame = ttk.Frame(master=container)
        top_frame.pack(side=side, anchor='nw')
        ttk.Label(master=top_frame, text=text).pack(anchor='nw')
        btn = MyButton(master=top_frame, width=22, text=getattr(AppManager.stg, stg_attr), command=update_dir)
        btn.pack(anchor='nw', padx=btn_pdx, pady=(0, 1))
