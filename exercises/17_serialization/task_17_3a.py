# -*- coding: utf-8 -*-
"""
Задание 17.3a

Создать функцию generate_topology_from_cdp, которая обрабатывает вывод
команды show cdp neighbor из нескольких файлов и записывает итоговую
топологию в один словарь.

Функция generate_topology_from_cdp должна быть создана с параметрами:
* list_of_files - список файлов из которых надо считать вывод команды sh cdp neighbor
* save_to_filename - имя файла в формате YAML, в который сохранится топология.
 * значение по умолчанию - None. По умолчанию, топология не сохраняется в файл
 * топология сохраняется только, если save_to_filename как аргумент указано имя файла

Функция должна возвращать словарь, который описывает соединения между устройствами,
независимо от того сохраняется ли топология в файл.

Структура словаря должна быть такой:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}},
 'R5': {'Fa 0/1': {'R4': 'Fa 0/1'}},
 'R6': {'Fa 0/0': {'R4': 'Fa 0/2'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.

Проверить работу функции generate_topology_from_cdp на списке файлов:
* sh_cdp_n_sw1.txt
* sh_cdp_n_r1.txt
* sh_cdp_n_r2.txt
* sh_cdp_n_r3.txt
* sh_cdp_n_r4.txt
* sh_cdp_n_r5.txt
* sh_cdp_n_r6.txt

Проверить работу параметра save_to_filename и записать итоговый словарь
в файл topology.yaml. Он понадобится в следующем задании.

"""

import re
from pprint import pprint
import yaml

def parse_sh_cdp_neighbors (input_str):
    r_string = r"(\S+)[>#]"
    match = re.search(r_string, input_str, re.DOTALL)
    if not match:
        return None
        
    device_name = match.group(1)
    
        
    r_string = r"(?P<device_id>\w+) +(?P<local_int>\S+ \S+) +\d+ +[\w ]+ +\S+ +(?P<port_int>\S+ \S+)"
    re_comp = re.compile(r_string)
    middle_dict = dict()
    for m in re.finditer(re_comp, input_str ):
        device_id, local_int, port_int= m.group("device_id", "local_int", "port_int")
        small_dict = dict()
        small_dict[device_id] = port_int
        middle_dict[local_int] = small_dict
     
    
    return (device_name,middle_dict)


def generate_topology_from_cdp(list_of_files, save_to_filename = None):
    res = dict()
    for file_name in list_of_files:
        with open("/home/vasily/pyneng/exercises/17_serialization/"+file_name,"r") as f:
            print(file_name)
            device,details = parse_sh_cdp_neighbors(f.read())
            res[device] = details
    
    if save_to_filename:
        with open(save_to_filename, "w") as f:
            yaml.dump(res,f)
    
    return res
        
files_list = {"sh_cdp_n_sw1.txt", 
              "sh_cdp_n_r1.txt",  
              "sh_cdp_n_r2.txt",
              "sh_cdp_n_r3.txt",
              "sh_cdp_n_r4.txt",
              "sh_cdp_n_r5.txt",
              "sh_cdp_n_r6.txt"}

generate_topology_from_cdp(files_list)