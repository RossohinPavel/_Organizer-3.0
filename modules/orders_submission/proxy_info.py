from ..app_manager import AppManagerR


class InfoProxy(AppManagerR):
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name):
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект"""
        order = cls.app_m.log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            res.order = order
            res.product_comp = {x.name: cls.app_m.lib.get_product_obj_from_name(x.name) for x in order.content}
            return res


class StickerGenProxy(InfoProxy):
    def create_sticker(self):
        main = []
        sub = {'+фото': None} if self.order.photo else {}
        for ed in self.order.content:
            line = ed.name
            prod = self.product_comp[line]
            if prod:
                short_name = prod.short_name
                if short_name.startswith('+'):
                    if short_name not in sub:
                        sub[short_name] = 0
                    sub[short_name] += ed.covers
                    continue
                line = ' '.join(tuple(self.__create_line(ed, prod)))
            main.append(line)
        return '\n'.join((*main, *(f'{k} {f"{v}шт" if v else ""}' for k, v in sub.items())))

    @staticmethod
    def __create_line(edition, prod_obj):
        short_name = prod_obj.short_name
        yield short_name
        if short_name not in ("Дуо", "Дуо гор", "Трио"):
            yield prod_obj.product_format
        yield edition.ccount if short_name not in ("Дуо", "Дуо гор", "Трио") else f'{(edition.covers)}шт'
        option = getattr(prod_obj, 'book_option', None)
        if option:
            yield option
        lamination = getattr(prod_obj, 'lamination', None)
        if lamination:
            yield lamination
        if edition.comp:
            yield f'-- {edition.comp}'
        if getattr(prod_obj, 'cover_type', None) == 'Кожаный корешок':
            yield '\nкож кор'
