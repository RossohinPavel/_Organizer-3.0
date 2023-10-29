import re


imgs = ['cover_001.jpg', 'cover_001-2_pcs.jpg', 'cover_1_pcs.jpg',
        '001__001.jpg', '001__001-2_pcs.jpg', '001_1_pcs.jpg']


for img in imgs:
    if re.fullmatch(r'(cover|\d{3})_{1,2}(\d{3}|-?\d+_pcs){1,2}\.jpg', img):
        print(img)
