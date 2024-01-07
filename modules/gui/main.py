from .source import *
from .source.style import style_init
from . import frames
from .menu_label import MenuLabel


class MainWindow(ttk.Window):
    """Основное окно приложения"""

    def __init__(self) -> None:
        super().__init__(title='Органайзер 3.5.0 BETA', iconphoto='data/assets/ico.png')
        # Запускаем определение стилей и получения изображений после __init__
        style_init()
        self.init_images()
        self.set_main_graph_settings()

        # Отрисовываем колонку меню
        menu_column = ttk.Frame(self)
        menu_column.pack(side=ttkc.LEFT, fill=ttkc.Y)

        self.todo = MenuLabel(
            'TODO', 
            menu_column, 
            # frames.PlanerFrame,
            ttk.Frame
        )
        self.todo.pack(anchor=ttkc.N)

        self.social = MenuLabel(
            'SOCIAL', 
            menu_column, 
            # frames.MailSamplesFrame,
            ttk.Frame
        )
        self.social.pack(anchor=ttkc.N)

        self.info = MenuLabel(
            'INFO', 
            menu_column, 
            # frames.InfoFrame
            ttk.Frame
            )
        self.info.pack(anchor=ttkc.N)

        self.file = MenuLabel(
            'FILE', 
            menu_column, 
            # frames.FileFrame
            ttk.Frame
        )
        self.file.pack(anchor=ttkc.N)

        self.stg = MenuLabel('SETTINGS', menu_column, frames.SettingsFrame)
        self.stg.pack(anchor=ttkc.S, expand=1, pady=(0, 5))

        # Разделитель
        ttk.Separator(self, orient='vertical').pack(side=ttkc.LEFT, fill=ttkc.Y)

        # Запускаем 1 фрейм - Лист задач
        self.todo.click(None)
    
    def init_images(self) -> None:
        """Ф-я, загружающая изображения."""
        from .source import images
        for k, v in images.__dict__.items():
            if not k.startswith('__'):
                setattr(images, k, ttk.PhotoImage(master=self, file=v))


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

    # def destroy(self) -> None:
    #     """Дополнительная логика при закрытии приложения. Проверяет есть ли активные задачи."""
    #     ttl = 'Очередь задач не пуста'
    #     msg = 'Закрытие программы во время обработки может привести к повреждению файлов.\nВы точно хотите это сделать?'
    #     if AppManager.queue.value > 0:
    #         if not tkmb.askokcancel(parent=self, title=ttl, message=msg):
    #             return
    #     super().destroy()
