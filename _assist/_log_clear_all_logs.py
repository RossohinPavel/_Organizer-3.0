import sqlite3
import os


for file in os.listdir(f'../data/logs'):
    os.remove(f'../data/logs/{file}')

with sqlite3.connect('../data/log.db') as connect:
    cursor = connect.cursor()
    cursor.execute('DELETE FROM LOG')