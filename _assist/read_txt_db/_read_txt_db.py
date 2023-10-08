import sqlite3
import pickle


MEM = {}

with open('mem.pcl', 'rb') as file:
    MEM.update(pickle.load(file))


def mem_func(line, db_str):
    if line[0] not in MEM:
        print('-' * 50)
        print(db_str[1], '--', db_str[3], '--', db_str[4], '--', db_str[-1])
        print('заменить на')
        print(line[0], '--', line[3], '--', line[4], '--', line[-1])
        print('-' * 50)
        command = input('command?  y/n :')
        if command not in 'yn':
            raise Exception('Принудительный выход')
        else:
            MEM[line[0]] = command
            with open('mem.pcl', 'wb') as file:
                pickle.dump(MEM, file)
    return MEM[line[0]]


with sqlite3.connect('../../data/log.db') as connect, open('OrdersReport.txt', 'r', encoding='utf-8') as file:
    cursor = connect.cursor()
    date = ''
    for line in file.readlines()[1:]:
        line = line.strip().split('\t')
        if line[0] == '304072':
            continue
        cursor.execute(f'SELECT * FROM Orders WHERE name={line[0]}')
        res = cursor.fetchone()
        if not res or line[0] == '304072':
            continue
        # command = mem_func(line, res)
        # command = 'y'
        # if command == 'y':
        if line[-1].find(',') != -1:
            line[-1] = line[-1].replace(',', '.')
            print(line)
        try:
            cursor.execute(f'UPDATE Orders '
                           f'SET customer_name=\'{line[3]}\', customer_address=\'{line[4]}\', price={float(line[-1])} '
                           f'WHERE name=\'{line[0]}\'')
            connect.commit()
            print(line[0])
        except Exception as error:
            print(error)
            print(line)
            input()
