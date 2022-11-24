### Cкрипт удаляет 50% изображений и аннотаций из датасета yolo, где присутствуют только объекты person

from pathlib import Path
data_type = 'train'
files = Path(f'/home/mosminin/fiftyone/coco-2017/labels/{data_type}/').glob('*.txt')
img_path = f'/home/mosminin/fiftyone/coco-2017/images/{data_type}'
name_list = list(map(str, files))
print(len(name_list), name_list[:3], sep='\n')
iters = 0

from tqdm.contrib.concurrent import process_map
import os
from time import time, sleep
from random import randrange

def process_file(file_name):
    global iters                  
    def chance(percent=50):  # вероятность
        return randrange(100) < percent
    
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
    rename = True
    data = []
    for each in lines: # Обрабатываем строки
        data.append(int(each.split()[0])) # Делаем список классов в формате int
    if sum(data) > 0: # Если сумма классов > 0 т.е. в пачке не только 'person', то отменяем перезапись
        rename = False
    if rename and chance: #  # Если назначена перезапись, то:
        # print(f'{iters} processed!')
        iters += 1
        rename_label(file_name)  #переименовать файл с анотациями
        rename_img(img_path, file_name) # переименовать файл с изображением
        #   переименовать файл с изображением
 
    file.close()
    # sleep(0.5)
   
if __name__ == '__main__':
   r = process_map(process_file, name_list, max_workers=4, chunksize=1)

# print(f'{iters} обработано!')