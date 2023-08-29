import tkinter as tk
import threading as th
import time


def f_sleep():
    for i in range(5, 0, -1):
        print(f"wait {i}")
        time.sleep(1)
    print('weak up')


def main():
    th1 = th.Thread(target=f_sleep)
    th1.start()


root = tk.Tk()
root.geometry('100x100')

txt = tk.Button(master=root, text='text', command=main)
txt.pack(anchor='center', expand=1)


root.mainloop()