import ttkbootstrap as ttk
from ttkbootstrap import PhotoImage


root = ttk.Window('test')

t = PhotoImage(file='../data/assets/home.png')

lst = ['t1', 't2']

val = ttk.StringVar(root)

r1 = ttk.Radiobutton(root, bootstyle='light-outline-toolbutton', image=t, variable=val, value='t1')

r2 = ttk.Radiobutton(root, bootstyle='outline-toolbutton', image=t, variable=val, value='t2')


r1.place(x=20, y=20)
r2.place(x=20, y=80)


root.mainloop()