# -*- coding: utf-8 -*-
"""
Задание 9.3

Создать функцию get_int_vlan_map, которая обрабатывает конфигурационный
файл коммутатора и возвращает кортеж из двух словарей:
* словарь портов в режиме access, где ключи номера портов,
  а значения access VLAN (числа):
{'FastEthernet0/12': 10,
 'FastEthernet0/14': 11,
 'FastEthernet0/16': 17}

* словарь портов в режиме trunk, где ключи номера портов,
  а значения список разрешенных VLAN (список чисел):
{'FastEthernet0/1': [10, 20],
 'FastEthernet0/2': [11, 30],
 'FastEthernet0/4': [17]}

У функции должен быть один параметр config_filename, который ожидает как аргумент
имя конфигурационного файла.

Проверить работу функции на примере файла config_sw1.txt

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
def get_int_vlan_map(config_filename):
    access_dict= dict()
    trunk_dict= dict()
    
    with open(config_filename, "r") as file:
        intf =""
        is_mode_trunk= None
        access_vlan = None
        trunk_vlans = list()

        for line in file:
            if line.startswith("interface"):
                intf= line.split()[1]
            elif line.startswith(" switchport mode access"):
                is_mode_trunk = False
            elif line.startswith(" switchport mode trunk"):
                is_mode_trunk = True
            elif line.startswith(" switchport access vlan"):
                access_vlan = int(line.split()[3])
            elif line.startswith(" switchport trunk allowed"):
                vlans_str= line.split()[4]
                trunk_vlans = [int(i) for i in vlans_str.split(",")]
            elif line.startswith("!"):
                if intf:
                    if is_mode_trunk:
                        trunk_dict[intf] =trunk_vlans
                    elif is_mode_trunk == False:
                        access_dict[intf] = access_vlan 
                intf =""
                is_mode_trunk= None
                access_vlan = None
                trunk_vlans = list()
        return access_dict, trunk_dict
    
    

access, trunk = get_int_vlan_map("/home/vasily/pyneng/exercises/09_functions/config_sw1.txt")
print(access)
print(trunk)