from dataclasses import dataclass


@dataclass
class Test:
    test: str = None
    __slot__ = 'test'


test = Test()

print(test.__dict__)
