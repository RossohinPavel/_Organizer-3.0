try:
    from Tkinter import Tk, Frame, Menu, Text, Label, END  # python2
except ImportError:
    from tkinter import Tk, Frame, Menu, Text, Label, END  # python3


class Main(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("context")
        label = Label(self.parent, text='какой то текст ')
        label.pack()
        self.text = Text(self.parent)
        self.text.pack()
        self.menu = Menu(self.text, tearoff=0)
        self.menu.add_command(label="Print Label text", command=lambda: label.config(text=self.text.get(1.0, END)))
        self.menu.add_command(label="Exit", command=lambda: self.close())
        self.text.bind("<Button-3>", lambda event: self.menu.post(event.x_root, event.y_root))
        self.pack()


if __name__ == '__main__':
    root = Tk()
    root.geometry('400x400')
    app = Main(root)
    root.mainloop()