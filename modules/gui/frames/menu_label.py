from ..source import *
from ...mytyping import Any, Type


class MenuLabel(ttk.Frame):
    """'Кнопка', для переключения страничек приложения"""
    current_frame = None

    def __init__(self, name: str, master: Any, frame: Type[ttk.Frame | ttk.LabelFrame]):
        super().__init__(master)

        # Имя виджета
        self._name = name

        # Виджет, который будет отрисовываться по нажатию на картинку
        self._frame = frame(master.master)

        # Основное изображение кнопки
        self._img = ttk.Label(self)
        self._img.pack()
        self._img.bind('<Button-1>', self.click)
        self._img.bind('<<ThemeChanged>>', self.on_theme_icon_change)
    
    def click(self, _) -> None:
        """"Срабатывание по клику мышкой на фрейм"""
        if self.current_frame != self:
            self.current_frame._frame.pack_forget()
            MenuLabel.current_frame = self
            self._frame.pack(side=ttkc.LEFT, expand=1, fill=ttkc.BOTH)
    
    def on_theme_icon_change(self, _):
        """Меняет иконку в след за изменением темы."""
        if not self._frame.winfo_viewable():
            suf = '_l' if AppManager.stg.theme == 'light' else '_d'
            self._img.configure(image=IMAGES[f'{self._name}{suf}'])
