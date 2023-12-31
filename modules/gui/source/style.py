from ttkbootstrap import Style


def style_init(name: str = '') -> None:
    """Ф-я для инициализации общих используемых стилей. Вызывается после инициализации основного объекта ttkbootstrap."""
    style = Style()

    if name:
        style.theme_use(name)
    # --------------Стили кнопок--------------

    # Стиль для кнопок выбора папок в меню. выравнивает текст по левому краю
    style.configure('l_jf.Outline.TButton', padding=(5, 2, 0, 2))
    style.layout(
        'l_jf.Outline.TButton', 
        [
            (
                'Button.border', 
                {
                    'sticky': 'nswe', 
                    'border': '1', 
                    'children': [
                        (
                            'Button.focus', 
                            {
                                'sticky': 'nswe', 
                                'children': [
                                    (
                                        'Button.padding', 
                                        {
                                            'sticky': 'nswe', 
                                            'children': [('Button.label', {'side': 'left'})]
                                            }
                                    )
                                ]
                            }
                        )
                    ]
                }
            )
        ]
    )

    # Стиль для маленьких кнопок в меню
    style.configure('minibtn.Outline.TButton', padding=2)

    # Стиль для свитчера тем
    style.configure('ts.Outline.TMenubutton', padding=(5, 2, 0, 2), width=15)

    # Стиль для кнопок текстовых шаблонов 
    style.configure('ms.info.Outline.TMenubutton', padding=(5, 2, 0, 2))

    # Стиль для кнопки + в библиотеке
    style.configure('Lib+.success.Outline.TButton', padding=(5, 1, 5, 1))

    # Стиль для кнопки копировать 📑 в библиотеке
    style.configure('Libcopy.success.Outline.TButton', padding=(1, 1, 2, 1))

    # Стиль для кнопки + в библиотеке
    style.configure('Libedit.warning.Outline.TButton', padding=(3, 1, 3, 1))

    # Стиль для кнопки + в библиотеке
    style.configure('Libdelete.danger.Outline.TButton', padding=(3, 1, 3, 1))

    # --------------Стили текстовых лейблов--------------

    # 'Жирный' стиль для текстовой метки
    style.configure('Bold.TLabel', font='TkDefaultFont 10 bold')
