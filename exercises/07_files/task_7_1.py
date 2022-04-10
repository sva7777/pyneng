# -*- coding: utf-8 -*-
"""
Задание 7.1

Обработать строки из файла ospf.txt и вывести информацию по каждой строке в таком
виде на стандартный поток вывода:

Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
templete = """
Prefix                {}
AD/Metric             {}
Next-Hop              {}
Last update           {}
Outbound Interface    {}
"""

with open("/home/vasily/pyneng/exercises/07_files/ospf.txt","r") as file:
    for line in file:
        line= line.replace(",","")
        line_dict= line.split()
        out_intf= line_dict[-1]
        last_update= line_dict[-2]
        next_hop = line_dict[-3]
        metric = line_dict[2].replace("[","").replace("]","")
        ip_mask = line_dict[1]
        print(templete.format(ip_mask,metric,next_hop, last_update,out_intf)) 