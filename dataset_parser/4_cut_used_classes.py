### Cкрипт удаляет 50% изображений и аннотаций из датасета yolo, где присутствуют только объекты person

exclude_list = ['0', '2', '3', '5', '7']
export_dir = '//home/mosminin/fiftyone/coco-all_yolo'

from pathlib import Path
data_type = 'validation'
files = Path(f'{export_dir}/labels/{data_type}/').glob('*.txt')
img_path = f'{export_dir}/images/{data_type}'
name_list = list(map(str, files))
# print(len(name_list), name_list[:3], sep='\n')
iters = 0

from tqdm.contrib.concurrent import process_map
import os
from time import time, sleep
from random import randrange

def process_file(file_name):
    global iters                  
    
    def rename_label(f_name, addition = '_'): # переименовывание файла
        name = Path(f_name)
        # print(f"TXT new fn: {name.parent}{name.stem}{name.suffix}{addition}" )
        name.rename(Path(name.parent, f"{name.stem}{name.suffix}{addition}")) #! Переименовываем файл
        
    def rename_img(img_path, file_name, addition = '_'): # переименовывание файла      
        txt_name = Path(file_name)
        img_name = Path(img_path, f'{txt_name.stem}.jpg')
        try:
            to_rename = Path(img_name.parent, f"{txt_name.stem}{img_name.suffix}_")
            # print(f'IMG name={img_name}, txt_name={txt_name.stem}, name_parent={img_name.parent} -> {to_rename}\n')
            os.rename(img_name, to_rename) #! Переименовываем файл
        except FileNotFoundError:
            # print(f'{to_rename} not found\n')
            pass
    
    ###
    # t_count.value = time() - t_count.value
    # p_count.value += 1
    # print(str(p_count.value)+'\n')
    ###
    file = open(file_name, 'r') # Читаем файл
    lines = file.readlines()
    rename = False
    for each in lines: # Обрабатываем строки
        cls = each.split()[0] # gПолучаем значение класса в строке
        if cls in exclude_list:
            # print(f'{iters}: removing {file_name}, class {cls}')
            rename = True
            break
    if rename: #  # Если назначена перезапись, то:
        # print(f'{iters} processed!')
        # iters += 1
        rename_label(file_name)  #переименовать файл с анотациями
        rename_img(img_path, file_name) # переименовать файл с изображением
        #   переименовать файл с изображением
 
    file.close()
    # sleep(0.5)
   
if __name__ == '__main__':
   r = process_map(process_file, name_list, max_workers=1, chunksize=1)

# print(f'{iters} обработано!')