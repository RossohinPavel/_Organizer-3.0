"""
    Собирает в себе импотры, 
    необходимые для работы осноных виджетов.
"""


# Базовый tkinter и его зависимые модули
import tkinter
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd

# Модерновый фреймворк ttkbootstrap и его модули
import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc
from ttkbootstrap.scrolled import ScrolledFrame
from ttkbootstrap import Querybox

# Типизация, используемая в большинстве виджетов
from typing import Any, Callable, Literal, Type

# AppManager управления приложением
from ...app_manager import AppManager
