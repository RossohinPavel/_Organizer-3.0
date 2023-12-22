# Базовый tkinter и его зависимые модули
import tkinter
from tkinter import messagebox as tkmb
from tkinter import filedialog as tkfd

# Модерновый фреймворк ttkbootstrap и его модули
import ttkbootstrap as ttk
import ttkbootstrap.constants as ttkc
from ttkbootstrap.scrolled import ScrolledFrame

# Типизация, используемая в большинстве виджетов
from ..mytyping import Any

# AppManager управления приложением
from ..app_manager import AppManager

# Стили
from .style import style_init

# Иконки
from .images import IMAGES
