import modules.windows.source as source


class StickGenFrame(source.LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Генератор наклеек', **kwargs)
