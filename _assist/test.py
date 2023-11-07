import hashlib
import time
import os


constant = 'D:\\тест\\Book\\2020-01-02\\250204\\Детсад-Фотокнига полиграфическая Layflat 20x30 верт 5-9 разворота\\Constant\\004_20_pcs.jpg'

variable = 'D:\\тест\\Book\\2020-01-02\\250204\\Детсад-Фотокнига полиграфическая Layflat 20x30 верт 5-9 разворота\\001\\cover_001.jpg'


def get_hash_md5(filename) -> str:
    """test"""
    with open(filename, 'rb') as f:
        m = hashlib.md5()   # test
        while True:
            data = f.read(32768)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


start = time.time()


edt = 'D:\\тест\\Book\\2020-01-02\\250204\\Детсад-Фотокнига полиграфическая Layflat 20x30 верт 5-9 разворота'
img_hash = get_hash_md5(constant)

for cat in os.listdir(edt):
    cat_path = f'{edt}\\{cat}'
    if os.path.isdir(cat_path):
        for file in os.listdir(cat_path):
            if img_hash == get_hash_md5(f'{cat_path}\\{file}'):
                print(f'{file}__s__')

print(time.time() - start)
