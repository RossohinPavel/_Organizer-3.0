from ....app_manager import AppManager
from typing import Self, Iterator
from ....data_base.log import Order, Edition


class InfoProxy:
    """Прокси-объект, содержащий в себе объект заказа и записи из библиотеки"""
    __slots__ = 'order', 'product_comp'

    def __new__(cls, order_name: str) -> Self | None:
        """Пытаемся получить объект заказа из лога. Если удается, то на его основе создаем прокси объект"""
        order = AppManager.log.get(order_name)
        if order is not None:
            res = super().__new__(cls)
            # ссылка на заказ
            res.order = order
            # Соответствующие тиражам продукты из библиотеки
            res.product_comp = tuple(AppManager.lib.get(x.name) for x in order.content)  # type: ignore
            return res
    
    def __init__(self, order_name: str) -> None:
        self.order: Order
        self.product_comp: tuple[AppManager.lib.Product, ...]


class StickerGenProxy(InfoProxy):
    """Прокси объект для генерации стикеров в заказе"""

    __slots__ = ()

    def create_sticker(self) -> str:
        """Основная ф-я генерации стикера"""
        # Основной список, куда будут добавляться сформированные строки.
        main = []

        # Вспомагательный список, куда добавляется фотопечать и другая продукция, отличная от книг.
        # У фото значение None, так как для фото не важно количество. Остальное будет подписано поштучно.
        sub = {'+фото': 0} if self.order.photo else {}

        # Перебираем тиражи
        for i, ed in enumerate(self.order.content):     #type: ignore
            line = ed.name                  # Получаем имя продукта
            prod = self.product_comp[i]     # Получаем соответствующий продукт

            # Если для этого имени есть продукт, то формируем для него стикер
            if prod:
                short_name = prod.short_name

                # Все продукты с приставкой + - сопроводительные. Их добавляем в sub
                if short_name.startswith('+'):
                    if short_name not in sub:
                        sub[short_name] = 0
                    sub[short_name] += ed.covers
                    continue
                
                # Для книг формируем "стикерное" представление
                line = ' '.join(tuple(self.__create_line(ed, prod)))
            
            # Имя добавиться в любом случае.
            main.append(line)
    
        return '\n'.join((*main, *(f'{k} {f"{v}шт" if v else ""}' for k, v in sub.items())))

    @staticmethod
    def __create_line(edition: Edition, prod_obj: AppManager.lib.Product) -> Iterator[str]:
        """Вспомагательная генераторная ф-я для формирования информации о тираже"""
        # 1) Получаем и передаем короткое имя
        short_name = prod_obj.short_name
        yield short_name

        # 2) Передаем формат для книг. Для продуктов типа Дуо это не нужно
        if short_name not in ("Дуо", "Дуо гор", "Трио"):
            yield prod_obj.product_format       #type: ignore

        # 3) Передаем колличественное представление. Для книг - комплексный счетчик, остальное - шутчно.
        if short_name in ("Дуо", "Дуо гор", "Трио"):
            yield f'{(edition.covers)}шт'
        else:
            yield edition.ccount                #type: ignore

        # 4) Для книг возвращаем опции сборки
        option = getattr(prod_obj, 'book_option', None)
        if option: yield option

        # 5) Для продуктов с ламинацией возвращаем ламинацию
        lamination = getattr(prod_obj, 'lamination', None)
        if lamination: yield lamination

        # 6) Если у тиража определилось совмещение (книг больше, чем 1), то возвращаем его.
        if edition.comp: yield f'-- {edition.comp}'

        # 7) Для типа обложки Кожаный корешок возвращаем дополнительную строку
        if getattr(prod_obj, 'cover_type', None) == 'Кожаный корешок': yield '\nкож кор'
