from ..source import *
from ...mytyping import Any, Type, Callable
from ...descriptors import Theme


class MenuLabel(ttk.Frame):
    """'Кнопка', для переключения страничек приложения"""
    current_frame = None

    def __init__(self, img_name: str, master: Any, frame: Type[ttk.Frame | ttk.LabelFrame]):
        super().__init__(master)
        # Основное изображение кнопки
        self._img = ttk.Label(self)
        self._img.pack()
        self._img.bind('<Button-1>', self.click)

        # Меняем отображение изображения по наведению мыши
        self._under_mouse = None
        Theme.add_call(self.change_under_mouse_img(img_name))
        self.bind('<Enter>', self.enter_event)
        self.bind('<Leave>', self.leave_event)

        self._off_img = IMAGES[f'{img_name}_off']
        self._on_img = IMAGES[f'{img_name}_on']

        # Виджет, который будет отрисовываться по нажатию на картинку
        self._frame = frame(master.master)
    
    def change_under_mouse_img(self, img_name: str) -> Callable[[str], None]:
        """Меняет изображение, которое оботражается по наведению мыши."""
        def inner(theme: str) -> None:
            match theme:
                case 'dark': suf = '_d'
                case 'light' | _: suf = '_l'
            self._under_mouse = IMAGES[f'{img_name}{suf}']
        
        return inner
    
    def enter_event(self, _) -> None:
        """Меняет изображение на _img при наведении мыши"""
        if not self._frame.winfo_viewable():
            self._img.configure(image=self._under_mouse)    # type: ignore
    
    def leave_event(self, _) -> None:
        if not self._frame.winfo_viewable():
            self._img.configure(image=self._off_img)    # type: ignore

    def click(self, _) -> None:
        """"Срабатывание по клику мышкой на фрейм"""
        if self.current_frame != self:
            self.current_frame._frame.pack_forget()                                 #type: ignore
            self.current_frame._img.configure(image=self.current_frame._off_img)    #type: ignore
            MenuLabel.current_frame = self
            self._img.configure(image=self._on_img)
            self._frame.pack(side=ttkc.LEFT, expand=1, fill=ttkc.BOTH)
