from ...source import *
from tkinter import Listbox


class AliasInterface:
    """Класс отрисовки виджетов и управления псевдонимами"""

    __slots__ = ('listbox', )

    def __init__(self, master: ttk.Frame) -> None:
        # Контейнер для лейбла и кнопок
        container = ttk.Frame(master)
        container.pack(anchor=ttkc.NW, pady=(0, 3), fill=ttkc.X)

        # Отрисовка Лейбла и кнопопк
        ttk.Label(container, text="Псевдонимы").pack(side=ttkc.LEFT)

        del_btn = ttk.Button(
            container,
            text='🗑', 
            style='Libdelete.danger.Outline.TButton',
            command=self.delete_command
        )
        del_btn.pack(side=ttkc.RIGHT, padx=(3, 0))

        add_btn = ttk.Button(
            container,
            text='+',
            style='Lib+.success.Outline.TButton',
            command=self.add_command
        )
        add_btn.pack(side=ttkc.RIGHT)

        #Листбокс
        self.listbox = Listbox(master)
        self.listbox.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        # Прокрутка листбокса
        sb = ttk.Scrollbar(
            master, 
            style='round',
            orient='vertical', 
            command=self.listbox.yview
        )
        sb.pack(side=ttkc.LEFT, fill=ttkc.Y)
        
        self.listbox.configure(yscrollcommand=sb.set)

    def add_command(self) -> None:
        """Добавление значения в Listbox по нажатию конопки."""
        pos = self.listbox.winfo_rootx() + 75, self.listbox.winfo_rooty() - 40

        # Оборачиваем в try, чтобы не кидало ошибку при закрытом дочернем окне.
        try:
            res = Querybox.get_string(
                prompt='Введите название псевдонима',
                title='Добавление псевдонима',
                parent=self.listbox,
                position=pos
            )
            if self.listbox.winfo_viewable() and res:
                self.insert(res)
        except: pass

    def delete_command(self) -> None:
        """Удаляет элемент по выбранному индексу"""
        try: self.listbox.delete(self.listbox.curselection())
        except: pass
    
    def get(self) -> tuple[str]:
        """Получение списка псевдонимов"""
        return self.listbox.get(0, ttkc.END)
    
    def insert(self, *args) -> None:
        """Вставка значения в Listbox с проверкой на дубликаты"""
        elements = self.listbox.get(0, ttkc.END)
        for value in args:
            if value not in elements:
                self.listbox.insert(ttkc.END, value)
