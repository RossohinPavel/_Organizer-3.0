from .._source import *
from .. import windows


def control_frame(master: ctk.CTkFrame) -> None:
    header = ctk.CTkFrame(master=master)
    ctk.CTkLabel(master=header, text='Управление приложением').pack(padx=25, anchor='nw')
    header.pack(fill='x', expand=1)
    ctk.CTkButton(master=master, text='Клиенты').pack()
    ctk.CTkButton(master=master, text='Библиотека').pack()
    ctk.CTkButton(master=master, text='Информация').pack()
    ctk.CTkButton(master=master, text='Настройки', command=lambda: windows.Settings(root_master)).pack()
