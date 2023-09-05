import modules


if __name__ == '__main__':
    root = modules.MainWindow()
    root.modules.update({'settings': modules.Settings(), 'library': modules.Library(), })
    root.mainloop()
