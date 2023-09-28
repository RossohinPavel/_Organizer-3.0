import modules.windows.source as source


class MailSamplesFrame(source.LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Текстовые шаблоны', **kwargs)
