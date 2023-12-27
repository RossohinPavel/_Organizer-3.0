from ttkbootstrap import Style


def style_init(name: str = '') -> None:
    """Ф-я для инициализации общих используемых стилей. Вызывается после инициализации основного объекта ttkbootstrap."""
    style = Style()

    if name:
        style.theme_use(name)
    # --------------Стили кнопок--------------

    # Стиль для кнопок выбора папок в меню. выравнивает текст по левому краю
    style.configure('l_jf.Outline.TButton', padding=(5, 2, 0, 2))
    style.layout('l_jf.Outline.TButton', [('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [('Button.focus', {'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'side': 'left'})]})]})]})])

    # Стиль для маленьких кнопок в меню
    style.configure('minibtn.Outline.TButton', padding=(2, 2, 2, 2))

    # Стиль для свитчера тем
    style.configure('ts.Outline.TMenubutton', padding=(5, 2, 0, 2), width=15)

    # Стиль для кнопок текстовых шаблонов 
    style.configure('ms.info.Outline.TMenubutton', padding=(5, 2, 0, 2),)

    # --------------Стили текстовых лейблов--------------

    # 'Жирный' стиль для текстовой метки
    style.configure('Bold.TLabel', font='TkDefaultFont 10 bold')




    # # Стиль для кнопки категорий в библиотеке
    # style.configure('library.TButton')
    # style.layout('library.TButton', [('Button.border', {'sticky': 'nswe', 'border': '1', 'children': [('Button.focus', {'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'side': 'left'})]})]})]})])

    # # Стиль для кнопки + в библиотеке
    # style.configure('LibraryPlus.TButton', font=('TkDefaultFont', 20), padding=(5, -5, 5, -5))

    # # Отладочный стиль для Frame
    # style.configure('db.TFrame', background='red')
