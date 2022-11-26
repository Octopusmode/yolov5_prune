### Cкрипт удаляет 50% изображений и аннотаций из датасета yolo, где присутствуют только объекты person

import_dir = '/home/mosminin/fiftyone/coco-2017'
export_dir = '/home/mosminin/fiftyone/coco_test'
count = 1000

from pathlib import Path
from tqdm.contrib.concurrent import process_map
import os
from time import time, sleep
from random import randrange

data_type = 'validation'
files = Path(f'{import_dir}/labels/{data_type}/').glob('*.txt')
img_path = f'{import_dir}/images/{data_type}'
export_list = list(map(str, files))
print('import', len(export_list), export_list[:3], sep=',')

data_type = 'train'
files = Path(f'{export_dir}/labels/train/').glob('*.txt')
img_path = f'/{export_dir}/images/train'
train_list = list(map(str, files))
print('train', len(train_list), train_list[:3], sep=',')

data_type = 'validation'
files = Path(f'{export_dir}/labels/validation/').glob('*.txt')
img_path = f'/{export_dir}/images/validation'
val_list = list(map(str, files))
print('validation', len(val_list), val_list[:3], sep=',')

print('\n')

iters = 0

def process_file(file_name):
    global iters, count
                    
    # def chance(percent=50):  # вероятность
    #     return randrange(100) < percent
        
    def rename_file(path, file_name, ext='.txt', pred = 't', add = ''): # переименовывание файла      
        name = Path(file_name).stem
        source_name = Path(path, f'{name}{ext}')  # путь\*.*
        new_name = Path(path, f'{pred}{name}{ext}{add}')  # путь\t*.*
        try:
            # print(f'{iters}: IMG name={name}, path={path}, in={source_name}, out={new_name}\n')
            os.rename(source_name, new_name) #! Переименовываем файл
        except FileNotFoundError:
            # print(f'{source_name} not found\n')
            pass
    
    for file_name in export_list:
        # sleep(0.5)
        
        if file_name not in train_list or file_name not in val_list:
            name = Path(file_name).stem
            print(iters, file_name, sep=':')
            iters += 1
            rename_file(export_dir + '/labels/validation', file_name, ext='.txt')
            rename_file(export_dir + '/images/validation', file_name, ext='.jpg')
            # переименовать jpg {export_dir}\images\validation
            # переименовать txt {export_dir}\labels\validation
    
   
# if __name__ == '__main__':
#    r = process_map(process_file, export_list, max_workers=1, chunksize=1)
process_file(export_list)

# print(f'{iters} обработано!')