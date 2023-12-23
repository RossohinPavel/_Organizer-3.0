import ttkbootstrap as ttk


root = ttk.Window('test', themename='litera')


values = ['1', '2', '3']

var = ttk.StringVar(root)


o = ttk.OptionMenu(root, var, None, *values)
o.place(x=10, y=10)




root.mainloop()
