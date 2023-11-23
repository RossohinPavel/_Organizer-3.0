import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox

 
root = ttk.Window()
root.title("METANIT.COM")
root.geometry("250x200") 

def func():
    t = Querybox.get_string()



test = ttk.Button(root, text='test', command=func)

test.pack()


root.mainloop()