import modules.windows.source as source


class PlanerFrame(source.LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Планировщик', **kwargs)