from .common import *


class PlanerFrame(LabeledFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, text='Планировщик', **kwargs)