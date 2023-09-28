from tkinter import *

root = Tk()

entry = Entry()
entry.pack()


def command():
    print("Cursor positon:", entry.index("insert"))
    if entry.selection_present():
        selection_from = entry.index("sel.first")
        selection_to = entry.index("sel.last")
        print(f"Selection from {selection_from} to {selection_to}")
        print("Selected text:", entry.get()[selection_from:selection_to])


button = Button(text="Press me", command=command)
button.pack()

root.mainloop()