# -*- coding: utf-8 -*-
"""
Задание 17.3

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa 0/1': {'R5': 'Fa 0/1'},
        'Fa 0/2': {'R6': 'Fa 0/0'}}}

Интерфейсы должны быть записаны с пробелом. То есть, так Fa 0/0, а не так Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
"""
import re
def parse_sh_cdp_neighbors (input_str):
    res = dict()
    r_string = r"(\S+)[>#]"
    match = re.search(r_string, input_str, re.DOTALL)
    if not match:
        return None
        
    device_name = match.group(1)
    
    
    
    r_string = (r"(?P<device_id>\S+) *(?P<local_int>\S+ \S+) *"\
                "(\d+) *\S \S \S *(\d+) *(?P<port_int>\S+ \S+)")
    re_comp = re.compile(r_string)
    middle_dict = dict()
    for m in re.finditer(re_comp, input_str ):
        device_id, local_int, port_int= m.group("device_id", "local_int", "port_int")
        small_dict = dict()
        small_dict[device_id] = port_int
        middle_dict[local_int] = small_dict
        
        
    res[device_name] = middle_dict

    return res

    

file_name= "/home/vasily/pyneng/exercises/17_serialization/sh_cdp_n_sw1.txt"

with open(file_name, "r") as f:
    file_context = f.read()
    parse_sh_cdp_neighbors(file_context)
    