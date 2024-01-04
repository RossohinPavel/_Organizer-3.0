from ...source import *
from ...source.order_name_validate_entry import ONVEntry
from ....data_base.info_proxy import StickerGenProxy


class StickerGenFrame(ttk.Frame):
    """Фрейм генерации стикера"""

    def __init__(self, master: Any, padding: int | tuple[int, ...]):
        super().__init__(master, padding=padding)   # type:  ignore
        HeaderLabel(self, text='Генератор наклеек').pack(fill=ttkc.X, pady=(0, 2))

        # Верхнаяя чать - Поле ввода
        ONVEntry(self, self.main).pack(fill=ttkc.X, pady=(0, 5))

        # Текстовое поле
        self.field = ttk.Text(self)
        self.field.pack(anchor=ttkc.NW, fill=ttkc.BOTH)

    def main(self, order_name: str) -> None:
        """После валидации введенного номера, обновляет лейбл"""
        # Очитка текстового поля
        self.field.delete('1.0', ttkc.END)
        
        # Пытаемся получить прокси объект
        proxy = StickerGenProxy(order_name)

        if proxy is None:
            self.field.insert('1.0', f'Не могу найти заказ {order_name}')
            return

        # Если заказ существует, формируем информацию и вставляем ее в текстовое поле
        self.field.insert('1.0', f'{proxy.order.name} - {proxy.order.customer_name}\n')
        sticker = proxy.create_sticker()
        self.field.insert(ttkc.END, sticker)

        self.clipboard_clear()
        self.clipboard_append(sticker)
