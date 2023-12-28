from ...source import *
from tkinter import Listbox, Variable


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
            style='Libdelete.danger.Outline.TButton'
        )
        del_btn.pack(side=ttkc.RIGHT, padx=(3, 0))

        add_btn = ttk.Button(
            container,
            text='+',
            style='Lib+.success.Outline.TButton'
        )
        add_btn.pack(side=ttkc.RIGHT)

        #Листбокс
        self.listbox = Listbox(master, listvariable=Variable(master, ['test1', 'test2']))
        self.listbox.pack(side=ttkc.LEFT, fill=ttkc.BOTH, expand=1)

        # Прокрутка листбокса
        sb = ttk.Scrollbar(
            master, 
            style='round',
            orient='vertical', 
            command=self.listbox.yview
        )
        sb.pack(side=ttkc.LEFT, fill=ttkc.Y)



        # # Контейнер для виджетов
        # Tableview(
        #     master, 
        #     coldata=['Псевдонимы'],
        #     rowdata=[*((f'test_{i}', ) for i in range(20))]
        # ).pack()


    # def draw_alias_widgets(self, master: ttk.Frame) -> None:
    #     """Отрисовка виджетов управления псевдонимами"""
    #     # Контейнер для ентри виджета и кнопки добавления псевдонима
    #     

    #     entry_line = ttk.Frame(master)
    #     entry_line.pack()

    #     ttk.Entry(entry_line).pack(side=ttkc.LEFT)
    #     ttk.Button(entry_line, text='Добавить').pack(side=ttkc.RIGHT)

    #     