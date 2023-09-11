import modules


if __name__ == '__main__':
    app_m = modules.MyDict()    # Используем MyDict, чтобы был доступ к значениям по атрибутам
    # Инициализируем и сохраняем в словаре модули без зависимостей
    app_m.stg = modules.Settings()  # Инициализируем настройки приложения
    app_m.cnst = modules.Constants()  # Инициализируем объект постоянных
    app_m.pln = modules.IPlanner()  # Инициализируем планировщик заданий
    app_m.txt_vars = modules.MyDict()   # Инициализируем объект для хранения текстовых переменных
    app_m.lbr = modules.Library()  # Инициализируем библиотеку
    # Инициализируем и сохраняем в словаре модули с зависимостями
    root = modules.MainWindow(app_m)  # Инициализируем основное окно
    app_m.mnt = modules.Monitor(app_m)  # Инициализируем объект слежения за заказами
    root.mainloop()
