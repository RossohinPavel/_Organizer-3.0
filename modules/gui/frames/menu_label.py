from ..source import *
from ...mytyping import Any, Type, Literal
from ...descriptors import Theme


class MenuLabel(ttk.Frame):
    """'Кнопка', для переключения страничек приложения"""
    current_frame = None

    def __init__(self, img_name: str, master: Any, frame: Type[ttk.Frame | ttk.LabelFrame]) -> None:
        super().__init__(master)
        MenuLabel.current_frame = self
        # Основное изображение кнопки
        self._img_name = img_name
        self._img = ttk.Label(self, image=IMAGES[img_name + '_off'])
        self._img.pack()
        self._img.bind('<Button-1>', self.click)

        # Подсветка неактивной кнопки. Зависит от выбранной темы
        self._backlight = None
        Theme.add_call(self.change_backlight)
        self.bind('<Enter>', self.enter_event)
        self.bind('<Leave>', self.leave_event)

        # Виджет, который будет отрисовываться по нажатию на картинку
        self._frame = frame(master.master)
    
    def click(self, _) -> None:
        """"Срабатывание по клику мышкой на фрейм"""
        # Когда основное окно неактивно
        if self.current_frame != self:
            # Сбрасываем отрисовку связанного с кнопкой фрейма - страничики
            self.current_frame._frame.pack_forget()     #type: ignore

            # Меняем положение кнопки на выключенный
            self.current_frame.image_switcher('off')    #type: ignore

            # В классе меняем ссылку на лейбл, для правильной работы виджетов
            MenuLabel.current_frame = self

            # Включаем текущий виджет
            self.image_switcher('on')
            self._frame.pack(side=ttkc.LEFT, expand=1, fill=ttkc.BOTH)
    
    def image_switcher(self, mode: Literal['on', 'off']) -> None:
        """Меняет изображение на кнопке"""
        self._img.configure(image=IMAGES[f'{self._img_name}_{mode}'])
    
    def change_backlight(self, theme: str) -> None:
        """Меняет изображение, которое оботражается по наведению мыши."""
        self._under_mouse = IMAGES[f'{self._img_name}_{theme}']
    
    def enter_event(self, _) -> None:
        """Меняет изображение на _img при наведении мыши"""
        if not self._frame.winfo_viewable():
            self._img.configure(image=self._backlight)    # type: ignore
    
    def leave_event(self, _) -> None:
        if not self._frame.winfo_viewable():
            self._img.configure(image=self._backlight)    # type: ignore


