# -*- coding: utf-8 -*-
"""
Задание 7.3b

Сделать копию скрипта задания 7.3a.

Переделать скрипт:
- Запросить у пользователя ввод номера VLAN.
- Выводить информацию только по указанному VLAN.

Пример работы скрипта:

Enter VLAN number: 10
10       0a1b.1c80.7000      Gi0/4
10       01ab.c5d0.70d0      Gi0/8

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
result = [] 

vlan_input = input("input vlan id :")

with open("/home/vasily/pyneng/exercises/07_files/CAM_table.txt","r") as file:
    for line in file:
        line_dict = line.split();
        if len(line_dict) == 4 and line_dict[0].isdigit() and line_dict[0] == vlan_input :
            result.append([int(line_dict[0]),line_dict[1],line_dict[3] ])
            

result.sort();
for line in result:
    print("{:10}{:20}{}".format(str(line[0]), line[1], line[2] ) )