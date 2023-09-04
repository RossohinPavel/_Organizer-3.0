import modules


if __name__ == '__main__':
    settings = modules.Settings()
    library = modules.Library()
    monitor = modules.Monitor(settings)
    root = modules.MainWindow(settings, library, monitor)
    root.mainloop()
