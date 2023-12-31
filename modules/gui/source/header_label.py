from .main import ttk, Any, ttkc


class HeaderLabel(ttk.Frame):
    """Фрейм - заголовок, с надписью и подчеркиванием."""

    def __init__(self, master: Any, text: str = '', **kwargs):
        super().__init__(master, height=16, **kwargs)
        # Разделитель
        sep = ttk.Separator(self, orient='horizontal')
        sep.place(relwidth=1.0, rely=0.40)
        # Лейбл с текстом
        self.lbl = ttk.Label(self, text=text, padding=(0, -4, 0, 0))
        self.lbl.place(x=15, y=0)
