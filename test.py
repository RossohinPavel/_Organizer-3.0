import tkinter as tk
import threading as th
import time


start = True

def func(func):
    global start
    value = 0
    while start:
        print(f'I\'am second thread. Value = {value}')
        value += 1
        func(text=value)
        time.sleep(2)


root = tk.Tk()
text = tk.Label(master=root, text='Some text')
text.place(x=1, y=1)

if __name__ == '__main__':
    thr = th.Thread(target=func, args=(text.config, ))
    thr.start()
    root.mainloop()
    start = False
