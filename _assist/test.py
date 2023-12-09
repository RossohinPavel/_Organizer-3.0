import ttkbootstrap as ttk


root = ttk.Window('test')

lf = ttk.LabelFrame(root, text='test')
lf.pack(padx=5, pady=5)

text = ttk.Label(lf, text='test')
text.pack()

lf.configure(text='test1')

root.mainloop()