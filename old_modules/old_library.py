class Library:
    def get_product_values(self, category: str, full_name: str) -> dict:
        """
        Метод для получения данных из бд в виде словаря
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        """
        keys = tuple(self.get_product_object(category).__dict__.keys())
        sql_req = ', '.join(f'\"{x}\"' for x in keys)
        self.__cursor.execute(f'SELECT {sql_req} FROM {category} WHERE full_name=\'{full_name}\'')
        values = self.__cursor.fetchone()
        return {keys[i]: values[i] for i in range(len(keys))}

    def check_unique(self, category: str, full_name: str) -> bool:
        """
        Метод для проверки продукта на дубликат.
        :param category: Категория продукта / название таблицы
        :param full_name: Имя продукта
        :return: True если продукта нет в бд и False, если есть.
        """
        self.__cursor.execute(f'SELECT * FROM {category} WHERE full_name=\'{full_name}\'')
        return not self.__cursor.fetchone()

    def add(self, category: str, product_dict: dict):
        """
        Метод добавления продукта в библиотеку
        :param category: Категория продукта / название таблицы
        :param product_dict: Словарь с сформированными значениями
        """
        keys = ', '.join(f'{x}' for x in product_dict.keys())
        values = ', '.join(f'\'{x}\'' if type(x) == str else f'{x}' for x in product_dict.values())
        self.__cursor.execute(f'INSERT INTO {category} ({keys}) VALUES ({values})')
        self.__db.commit()

    def change(self, category: str, full_name: str, values: dict):
        """
        Внесение изменений в ячейку
        :param category:  Категория продукта / название таблицы
        :param full_name: Имя продукта
        :param values: Словарь с новыми значениями
        """
        sql_req = ', '.join(f'{k} = \"{v}\"' if type(v) == str else f'{k} = {v}' for k, v in values.items())
        self.__cursor.execute(f'UPDATE {category} SET {sql_req} WHERE full_name=\'{full_name}\'')
        self.__db.commit()
