import modules.windows.source as source
from modules.app_manager import AppManagerW


class ProcessingFrame(AppManagerW):
    def __init__(self, frame):
        self._frame = frame
        self.header = source.tk.StringVar(master=frame)
        self.status = source.tk.StringVar(master=frame)
        self.qty = source.tk.StringVar(master=frame)
        self.pb = source.ttk.Progressbar(master=frame, orient='horizontal', length=258)
        self._widgets = [source.ttk.Label(master=self._frame, textvariable=self.header, width=42),
                         source.ttk.Label(master=self._frame, textvariable=self.status, width=42),
                         source.ttk.Label(master=self._frame, textvariable=self.qty, width=42),
                         self.pb]


    def __enter__(self):
        self.header.set('__Имя модуля/номер заказа__')
        self.status.set('__Статус/имя тиража__')
        self.qty.set('__Количество__')
        self.pb['maximum'] = 0
        self.pb['value'] = 0
        place = 4
        for widget in self._widgets:
            widget.place(x=2, y=place)
            place += 24
            

    def __exit__(self, *args):
        for widget in self._widgets:
            widget.place_forget()
        
