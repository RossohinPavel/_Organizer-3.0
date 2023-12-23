from ..source import *
from ...mytyping import Any, Type


class MenuLabel(ttk.Frame):
    """'Кнопка', для переключения страничек приложения"""
    current_frame = None

    def __init__(self, name: str, master: Any, frame: Type[ttk.Frame | ttk.LabelFrame]):
        super().__init__(master)
        # Имя виджета
        self._name = name

        # Основное изображение кнопки
        self._img = ttk.Label(self)
        self._img.pack()
        self._img.bind('<Button-1>', self.click)

        self._off_img = IMAGES[f'{self._name}_off']
        self._on_img = IMAGES[f'{self._name}_on']

        # Виджет, который будет отрисовываться по нажатию на картинку
        self._frame = frame(master.master)
    
    def click(self, _) -> None:
        """"Срабатывание по клику мышкой на фрейм"""
        if self.current_frame != self:
            self.current_frame._frame.pack_forget()
            self.current_frame._img.configure(image=self.current_frame._off_img)
            MenuLabel.current_frame = self
            self._img.configure(image=self._on_img)
            self._frame.pack(side=ttkc.LEFT, expand=1, fill=ttkc.BOTH)
