import pickle
import os


for pcl_file in os.listdir(f'../data/logs'):
    with open(f'../data/logs/{pcl_file}', 'rb') as file:
        lst = pickle.load(file)
        for obj in lst:
            for slot in obj.__slots__:
                print(slot, '--', getattr(obj, slot))
