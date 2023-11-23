import ttkbootstrap as tb


 
root = tb.Window()
root.geometry("250x200") 

var = tb.StringVar(root)

t = tb.Menubutton(root, text='test')
t.pack()

im = tb.Menu(t)


im.add_command(label='test')
t['menu'] = im

def func(*args):
    global im
    print('sss')
    im.destroy()


def func1(*args):
    global im
    print('33')
    im = tb.Menu(t)
    im.add_command(label='test')
    t['menu'] = im
    t.event_generate('<<Invoke>>')



t.bind('<ButtonPress-1>', func)
t.bind('<ButtonPress-3>', func1)



root.mainloop()