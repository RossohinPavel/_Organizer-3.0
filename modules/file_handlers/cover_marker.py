from ._handler import Handler
from PIL import Image, ImageDraw, ImageFont


# def get_covers_from_comparison(path: str, comp: str | None) -> tuple:
#     """Возвращает кортеж, В котором находятся обложки согласно совмещению"""
#     target = 'Covers'
#     if comp in ('Копии', 'О_О'):
#         target = 'Constant'
#     return tuple(f'{target}/{c}' for c in os.listdir(f'{path}/{target}') if re_fullmatch(r'cover_(\d{3}|\d+_pcs)\.jpg', c))


class CoverMarkerHandler(Handler):
    def get_processing_frame_header(self) -> str:
        return f'Разметка обложек в заказе {self.proxy.name}'


    # def __call__(self, obj, **kwargs):
    #     print(obj)
        # self.storage.pf.header.set(f'Обработка обложек в заказе {obj.order}')
        # for edt, prd in obj.target.items():
        #     src_path = f'{self.storage.stg.z_disc}/{obj.creation_date}/{obj.order}/{edt.name}'
        #     dst_path = f'{self.storage.stg.o_disc}/{obj.creation_date}/{obj.order}/{edt.name}'
        #     for cover_name in self.get_covers_from_comparison(src_path, edt.comp):
        #         self.storage.pf.status.set(f'{cover_name}')
        #         with Image.open(f'{src_path}/{cover_name}') as cover_img:
        #             cover_img.load()
        #         cwidth, cheight = cover_img.width, cover_img.height
        #         draw_name = f'{cwidth}x{cheight}={prd.full_name}'
        #         draw_obj = self.cache.get(draw_name, None)
        #         if draw_obj is None:
        #             p_clapan = self.mm_to_pixel(prd.cover_clapan)
        #             p_joint = self.mm_to_pixel(prd.cover_joint)
        #             p_clength = self.mm_to_pixel(prd.carton_length)
        #             draw_obj = cover_img
        #             draw = ImageDraw.Draw(draw_obj)
        #             draw.rectangle((0, 0, cwidth, cheight), fill='#FFFFFF')     # Заливка белым
        #             draw.rectangle((p_clapan, p_clapan, p_clapan + p_clength, cheight - p_clapan), outline='#000000')
        #             draw.rectangle((cwidth - p_clapan, p_clapan, cwidth - p_clapan - p_clength, cheight - p_clapan), outline='#000000')
        #             main_line = p_clapan + p_clength + p_joint
        #             draw.rectangle((main_line, p_clapan, cwidth - main_line, cheight - p_clapan), outline='#000000')
        #             draw.rectangle((main_line, p_clapan + 150, cwidth - main_line, cheight - p_clapan - 150), fill='#FFFFFF')
        #             self.cache[draw_name] = cover_img
        #         draw_obj.save(f'{dst_path}/{cover_name[:-4]}_1.jpg', quality='keep', dpi=(300, 300))
        # self.cache.clear()