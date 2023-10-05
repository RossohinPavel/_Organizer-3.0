from modules.app_manager import AppManagerR


class OrderProxy(AppManagerR):
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name):
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект"""
        order = cls.app_m.log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            res.order = order
            res.product_comp = {x.name: cls.app_m.lib.get_product_obj_from_name(x.name) for x in order.content}
            return res


class StickerGenProxy(OrderProxy):
    def create_sticker(self):
        main = []
        sub = {'+фото': None} if self.order.photo else {}
        for ed in self.order.content:
            line = ed.name
            prod = self.product_comp[line]
            if prod:
                if prod.short_name.startswith('+'):
                    sub[prod.short_name] += ed.covers
                    continue
                line = ' '.join(tuple(self.__create_line(ed, prod)))
            main.append(line)
        return '\n'.join((*main, *(f'{k} {f"{v}шт" if v else ""}' for k, v in sub.items())))

    def __create_line(self, edition, prod_obj):
        short_name = prod_obj.short_name
        yield short_name
        if short_name not in ("Дуо", "Дуо гор", "Трио"):
            yield prod_obj.product_format
        yield edition.ccount if short_name not in ("Дуо", "Дуо гор", "Трио") else f'{(edition.covers)}шт'
        option = getattr(prod_obj, 'book_option', None)
        if option:
            yield option
        yield prod_obj.lamination
        if edition.comp:
            yield f'-- {edition.comp}'
