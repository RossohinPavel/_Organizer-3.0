from os import listdir
from os.path import isdir
from shutil import rmtree


def recursive_deleting(path: str) -> None:
    for cat in listdir(path):
        if cat == '__pycache__':
            rmtree(f'{path}/__pycache__')
        else:
            if isdir(path + '/' + cat):
                recursive_deleting(path + '/' + cat)


if __name__ == '__main__':
    recursive_deleting(__file__.rsplit('\\', maxsplit=3)[0])
