class CoverHandler:
    class_attr = 'class_attr'

    def __init__(self):
        self.__name__ = self.__class__.__name__
        self.__doc__ = self.__class__.__doc__

    def __call__(self, *args, **kwargs):
        print(self.class_attr)
        print(args, kwargs)


class CoverMarkerHandler(CoverHandler):
    pass