from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")

position = {"padx": 6, "pady": 6, "anchor": NW}

python = "Python"
java = "Java"
javascript = "JavaScript"

lang = StringVar(value=java)  # по умолчанию будет выбран элемент с value=java

header = ttk.Label(textvariable=lang)
header.pack(**position)

python_btn = ttk.Radiobutton(text=python, value=python, variable=lang)
python_btn.pack(**position)

javascript_btn = ttk.Radiobutton(text=javascript, value=javascript, variable=lang)
javascript_btn.pack(**position)

java_btn = ttk.Radiobutton(text=java, value=java, variable=lang)
java_btn.pack(**position)

root.mainloop()