from gui._source import *
from typing import Literal


class Settings(ChildWindow):
    """Окно основных настроек приложения"""
    win_title = 'Настройки'
    win_geometry = Geometry('345x288', '295x352')

    def main(self, *args, **kwargs) -> None:
        self.show_log_check_depth_widgets()
        self.show_directory_widgets()
        ctk.CTkButton(master=self, text='Закрыть', command=self.destroy).pack(anchor='se', pady=5, padx=5)

    def show_log_check_depth_widgets(self) -> None:
        """Отрисовка виджетов для настройки глубины проверки лога"""
        msg = ('Рекомендуемая глубина ~ 100 заказов.', 'Ограничено свободным объемом ОЗУ.')

        def get_entry_value(event: tkinter.Event | None = None) -> None:
            value = entry_var.get()
            if value.isdigit():
                AppManager.stg.log_check_depth = int(value)
                update_label()
            entry.delete(0, 'end')

        def update_label() -> None:
            value_lbl.configure(text=f'Текущее значение: {AppManager.stg.log_check_depth} заказов (папок)')

        header = ctk.CTkFrame(master=self)
        header.pack(fill='x', expand=1)
        ctk.CTkLabel(master=header, text='Глубина проверки лога').pack(anchor='nw', padx=25)
        value_lbl = ctk.CTkLabel(master=self)
        value_lbl.pack(anchor='nw', padx=5)
        update_label()
        frame = ctk.CTkFrame(master=self, fg_color='transparent')
        frame.pack(fill='x', expand=1)
        entry_var = ctk.StringVar(master=self)
        entry = ctk.CTkEntry(master=frame, textvariable=entry_var)
        entry.bind('<Return>', get_entry_value)
        entry.pack(side='left', padx=5, fill='x', expand=1)
        btn = ctk.CTkButton(master=frame, text='Задать', command=get_entry_value)
        btn.pack(side='right', expand=1, fill='x', padx=(0, 5))
        ctk.CTkLabel(master=self, text='\n'.join(msg)).pack(anchor='nw', padx=5)

    def show_directory_widgets(self) -> None:
        """Сборная ф-я для отрисовки виджетов управления папками заказов"""
        header = ctk.CTkFrame(master=self)
        header.pack(fill='x', expand=1)
        ctk.CTkLabel(master=header, text='Рабочие директории').pack(anchor='nw', padx=25)
        self.show_directory_frame('Диск операторов фотопечати \'Т\'', 't_disc')
        self.show_directory_frame('Диск загрузки заказов \'Z\'', 'z_disc')
        self.show_directory_frame('Диск печати заказов \'О\'', 'o_disc')

    def show_directory_frame(self, text: str, stg_attr: str) -> None:
        """Отрисовка виджетов управления рабочими папками"""
        def update_dir() -> None:
            path = tkfd.askdirectory(parent=self, initialdir=getattr(AppManager.stg, stg_attr), title=f'Выберите: {text}')
            if path:
                setattr(AppManager.stg, stg_attr, path)
                btn.configure(text=getattr(AppManager.stg, stg_attr))
        
        ctk.CTkLabel(master=self, text=text).pack(anchor='nw', padx=5)
        btn = ctk.CTkButton(master=self, text=getattr(AppManager.stg, stg_attr), command=update_dir)
        btn.pack(fill='x', expand=1, padx=5)
