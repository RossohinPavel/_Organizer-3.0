import tkinter as tk
import threading as th
import time


start = True

def func(func):
    global start
    value = 0
    while start:
        value += 1
        func(text=value)
        time.sleep(2)


def create_child():
    child = tk.Toplevel(root)
    child.focus_set()
    child.grab_set()


root = tk.Tk()
text = tk.Label(master=root, text='Some text')
text.place(x=1, y=1)
button = tk.Button(master=root, text='Create_child_window', command=create_child)
button.place(x=1, y=22)

if __name__ == '__main__':
    thr = th.Thread(target=func, args=(text.config, ))
    thr.start()
    root.mainloop()
    start = False
