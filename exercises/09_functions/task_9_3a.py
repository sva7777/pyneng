# -*- coding: utf-8 -*-
"""
Задание 9.3a

Сделать копию функции get_int_vlan_map из задания 9.3.

Дополнить функцию: добавить поддержку конфигурации, когда настройка access-порта
выглядит так:
    interface FastEthernet0/20
        switchport mode access
        duplex auto

То есть, порт находится в VLAN 1

В таком случае, в словарь портов должна добавляться информация, что порт в VLAN 1
Пример словаря:
    {'FastEthernet0/12': 10,
     'FastEthernet0/14': 11,
     'FastEthernet0/20': 1 }

У функции должен быть один параметр config_filename, который ожидает
как аргумент имя конфигурационного файла.

Проверить работу функции на примере файла config_sw2.txt

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
                        if access_vlan:
                            access_dict[intf] = access_vlan 
                        else:
                            access_dict[intf] = 1 
                intf =""
                is_mode_trunk= None
                access_vlan = None
                trunk_vlans = list()
        return access_dict, trunk_dict
    
    

access, trunk = get_int_vlan_map("/home/vasily/pyneng/exercises/09_functions/config_sw2.txt")
print(access)
print(trunk)