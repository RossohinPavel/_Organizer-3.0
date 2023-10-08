import pickle
import sqlite3


MEM = {}


def get_solutions(line):
    if line[1] not in MEM:
        print(line)
        sol = input('Вы хотите обновить данные для этого заказа (y/n/q)?')
        if sol == 'y':
            return sol
        if sol == 'n':
            MEM[line[1]] = sol
            with open('solutions.mem', 'wb') as file:
                pickle.dump(MEM, file)
        else:
            raise Exception('Выход из программы')
    return MEM[line[1]]


def get_new_data(line):
    print(f"Введите новое имя вместо <{line[-3]}>")
    customer_name = input()
    print(f"Введите новый адрес вместо <{line[-2]}>")
    customer_address = input()
    print(f"Введите новую сумму вместо <{line[-1]}>")
    price = float(input())
    return *line[:3], customer_name, customer_address, price


with open('solutions.mem', 'rb') as file:
    MEM.update(pickle.load(file))


with sqlite3.connect('../../data/log.db') as connect:
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM Orders WHERE customer_name="Unknown" OR customer_name="Диспетчер ФотокнигиОптом" OR price=0.0')
    for line in cursor.fetchall():
        if get_solutions(line) == 'y':
            new_line = get_new_data(line)
            cursor.execute(f'UPDATE Orders SET customer_name=\'{new_line[-3]}\', customer_address=\'{new_line[-2]}\', price={new_line[-1]} WHERE name=\'{line[1]}\'')
            connect.commit()
