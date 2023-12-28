import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview


root = ttk.Window()

row = []
row.append(('test', ))
row.append(('test', ))

t = Tableview(root, coldata=['Псевдонимы'], rowdata=row)
t.pack()



print(*(x.values for x in t.tablerows))


root.mainloop()