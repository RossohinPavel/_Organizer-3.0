from .source import *
from . import frames
from .menu_label import MenuLabel


class MainWindow(ttk.Window):
    """Основное окно приложения"""

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.4.2 BETA', iconphoto='data/assets/ico.png')
        # Запускаем определение стилей и получения изображений после __init__
        style_init()
        for k, v in IMAGES.items():
            IMAGES[k] = ttk.PhotoImage(master=self, file=v) #type: ignore
        self.set_main_graph_settings()

        # Отрисовываем колонку меню
        menu_column = ttk.Frame(self)
        menu_column.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.todo = MenuLabel('todo', menu_column, frames.PlanerFrame)
        self.todo.pack(anchor=ttkc.N)

        self.social = MenuLabel('social', menu_column, frames.MailSamplesFrame)
        self.social.pack(anchor=ttkc.N)

        self.info = MenuLabel('info', menu_column, frames.InfoFrame)
        self.info.pack(anchor=ttkc.N)

        self.file = MenuLabel('file', menu_column, frames.FileFrame)
        self.file.pack(anchor=ttkc.N)

        self.stg = MenuLabel('settings', menu_column, frames.SettingsFrame)
        self.stg.pack(anchor=ttkc.S, expand=1, pady=(0, 5))

        # Разделитель
        ttk.Separator(self, orient='vertical').pack(side=ttkc.LEFT, fill=ttkc.Y)

        # Запускаем 1 фрейм - Лист задач
        self.todo.click(None)

    def set_main_graph_settings(self) -> None:
        """Основные настройки окна, положения и размера."""
        width, height = 550, 350
        self.geometry(f'{width}x{height}+{(self.winfo_screenwidth()-width)//2}+{(self.winfo_screenheight()-height)//2}')
        self.resizable(False, False)
        self.bind_all('<Control-KeyPress>', self.russian_hotkeys)
        self.update_idletasks()

    @staticmethod
    def russian_hotkeys(event: tkinter.Event) -> None:
        """Эвент для срабатывания Ctrl+V на русской раскладке"""
        if event.keycode == 86 and event.keysym == '??':
            event.widget.event_generate('<<Paste>>')

    def destroy(self) -> None:
        """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
        ttl = 'Очередь задач не пуста'
        msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
        if AppManager.queue.value > 0:
            if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
                return
        super().destroy()
