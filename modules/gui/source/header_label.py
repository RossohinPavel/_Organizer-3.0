from .main import ttk, Any, ttkc


class HeaderLabel(ttk.Frame):
    """Фрейм - заголовок, с надписью и подчеркиванием."""

    def __init__(self, master: Any, text: str, /, **kwargs):
        super().__init__(master)
        # Разделитель
        sep = ttk.Separator(self, orient='horizontal')
        sep.place(relwidth=1.0, rely=0.42)
        # Лейбл с текстом
        lbl = ttk.Label(
            self, 
            text=text, 
            padding=(0, -4, 0, -2)
        )
        lbl.pack(anchor=ttkc.W, padx=(15, 0))
