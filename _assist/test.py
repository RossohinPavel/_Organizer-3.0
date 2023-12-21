from enum import verify
import ttkbootstrap as ttk


class Main(ttk.Frame):
    def __init__(self, master, /, **kwargs):
        super().__init__(master, **kwargs)
        self.lbl = ttk.Label(self, image=t)
        self.lbl.pack(side='left')
        self.support = ttk.Label(self)
        self.support.pack(side='left', fill='y')

        self.lbl.bind('<Button-1>', self.event)

        self.bind('<<ThemeChanged>>', self.event)

    def event(self, e):
        style.theme_use('darkly')
        print(e)


root = ttk.Window('test', themename='litera')

t = ttk.PhotoImage(master=root, file='../data/assets/settings_l.png')

m = Main(root)
m.pack(side='left')

ttk.Separator(root, orient='vertical').pack(side='left')
# root.winfo_children()[0].destroy()

style = ttk.Style()



root.mainloop()
