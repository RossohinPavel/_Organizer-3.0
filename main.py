import modules


if __name__ == '__main__':
    # Инициализируем модули без зависимостей
    modules.Constants()  # Инициализируем объект постоянных
    modules.Settings()  # Инициализируем настройки
    modules.Library()  # Инициализируем библиотеку
    root = modules.MainWindow()  # Инициализируем основное окно. Оно добавит в app_m текстовые переменные для модулей
    # Инициализируем модули с зависимостями
    modules.IPlanner()  # Инициализируем планировщик заданий
    modules.OrdersTracker()  # Инициализируем объект слежения за заказами
    root.mainloop()
