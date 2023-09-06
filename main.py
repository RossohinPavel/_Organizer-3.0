import modules


if __name__ == '__main__':
    app_m = modules.MyDict()
    app_m.pln = modules.IPlanner()  # Инициализируем планировщик заданий
    app_m.cnst = modules.Constants()    # Инициализируем объект постоянных
    app_m.txt_vars = modules.MyDict()   # Инициализируем объект для хранения текстовых переменных
    app_m.stg = modules.Settings()  # Инициализируем настройки приложения
    app_m.lbr = modules.Library()  # Инициализируем библиотеку
    root = modules.MainWindow(app_m)  # Инициализируем основное окно
    app_m.mnt = modules.Monitor(app_m)  # Инициализируем объект слежения за заказами
    root.mainloop()
