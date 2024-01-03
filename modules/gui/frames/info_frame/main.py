from ...source import *
from .stickergen_frame import StickerGenFrame
from .tracker_frame import TrackerFrame


class InfoFrame(ttk.Frame):
    """Фрейм с отображением различной информации."""

    def __init__(self, master: Any) -> None:
        super().__init__(master)

        left = StickerGenFrame(self, (5, 5, 3, 5))
        left.place(x=0, y=0, relwidth=0.6, relheight=1)

        right = TrackerFrame(self, (3, 5, 5, 5))
        right.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)
        self.draw_info_frame(right)
    
    def draw_info_frame(self, master: Any) -> None:
        """Отрисовка кнопок информации"""
        lbl = HeaderLabel(master, text='Информация', anchor='n')
        lbl.pack(fill=ttkc.X, expand=1, anchor=ttkc.S)
        b1 = ttk.Button(
            master, 
            style='minibtn.Outline.TButton',
            text='Заказы', 
            # command=None
        )
        b1.pack(fill=ttkc.X, pady=(2, 5))
        b2 = ttk.Button(
            master, 
            style='minibtn.Outline.TButton',
            text='Клиенты', 
            # command=lambda: print(b1.winfo_geometry())
        )
        b2.pack(fill=ttkc.X)
