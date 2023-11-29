import ttkbootstrap as ttk


root = ttk.Window()

btn = ttk.Button(root, text='test')
btn.place(x=5, y=5)

root.bind("<Button-4>", lambda e: print(e))
root.bind("<Button-5>", lambda e: print(e))

root.mainloop()