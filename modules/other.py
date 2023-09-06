class MyDict(dict):
    __getattribute__ = dict.get
    __setattr__ = dict.__setitem__
