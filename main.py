import modules
import threading
import time


def init_autolog(app_stg):
    while app_stg.is_alive:
        print('i am autolog')
        time.sleep(2)


if __name__ == '__main__':
    settings = modules.Settings()
    root = modules.MainWindow(settings)
    if settings.autolog:
        autolog_thread = threading.Thread(target=init_autolog, args=(settings, ))
        autolog_thread.start()
    root.mainloop()
    settings.is_alive = False
