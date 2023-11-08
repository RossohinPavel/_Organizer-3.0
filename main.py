from modules import *


if __name__ == '__main__':
    # Инициализируем модули без зависимостей
    lib = Library()
    log = Log()
    root = MainWindow()
    # modules.TaskManager()  # Инициализируем планировщик заданий

    # root = modules.MainWindow()  # Инициализируем основное окно. Оно добавит в app_m текстовые переменные для модулей
    # # # Инициализируем модули с зависимостями
    # # modules.init_trackers()  # Инициализируем объект контейнер трекеров
    # # modules.Settings()  # Инициализируем настройки
    root.mainloop()
