from PIL import Image, ImageDraw


with Image.open(f'D:\\тест\\Book\\2020-01-03\\250308\\1 ШКОЛА 4 В-Фотоальбом полиграфический 20x30 верт\\Constant\\003_5_pcs.jpg') as test_img:
    test_img.load()
l_side = test_img.crop((0, 0, test_img.width // 2, test_img.height))
l_side.show()
