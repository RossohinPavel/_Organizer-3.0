import modules
import threading as th
import time


def init_autolog():
    while settings.is_alive:
        monitor.run()
        time.sleep(4)


if __name__ == '__main__':
    settings = modules.Settings()
    library = modules.Library()
    monitor = modules.Monitor(settings)
    root = modules.MainWindow(settings, library, monitor)
    if settings.autolog:
        th1 = th.Thread(target=init_autolog)
        th1.start()
    root.mainloop()
    settings.is_alive = False
