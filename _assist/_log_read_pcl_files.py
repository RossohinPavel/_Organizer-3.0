import pickle
import os
import time


for pcl_file in os.listdir(f'../data/logs'):
    with open(f'../data/logs/{pcl_file}', 'rb') as file:
        lst = pickle.load(file)
        for obj in lst:
            for slot in obj.__slots__:
                if slot == 'photo':
                    photo = getattr(obj, slot)
                    if photo is None:
                        print(slot, '--', photo)
                    else:
                        print(slot, '--')
                        for key, val in photo.matrix_repr.items():
                            print(f'--{key}-{val}')
                if slot == 'content':
                    print(slot, '--')
                    for con in obj.content:
                        print(f'--{con.name}')
                        print(f'----{con.matrix_repr}')
                if slot not in ('photo', 'content'):
                    print(slot, '--', getattr(obj, slot))
