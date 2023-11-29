import ttkbootstrap as ttk


root = ttk.Window()

lbl1 = ttk.Label(root, text='test1')
lbl1.pack()

lbl1.pack_forget()

lbl2 = ttk.Label(root, text='test2')
lbl2.pack()

lbl1.pack()

root.mainloop()