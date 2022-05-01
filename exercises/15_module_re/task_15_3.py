# -*- coding: utf-8 -*-
"""
Задание 15.3

Создать функцию convert_ios_nat_to_asa, которая конвертирует правила NAT
из синтаксиса cisco IOS в cisco ASA.

Функция ожидает такие аргументы:
- имя файла, в котором находится правила NAT Cisco IOS
- имя файла, в который надо записать полученные правила NAT для ASA

Функция ничего не возвращает.

Проверить функцию на файле cisco_nat_config.txt.

Пример правил NAT cisco IOS
ip nat inside source static tcp 10.1.2.84 22 interface GigabitEthernet0/1 20022
ip nat inside source static tcp 10.1.9.5 22 interface GigabitEthernet0/1 20023

И соответствующие правила NAT для ASA:
object network LOCAL_10.1.2.84
 host 10.1.2.84
 nat (inside,outside) static interface service tcp 22 20022
object network LOCAL_10.1.9.5
 host 10.1.9.5
 nat (inside,outside) static interface service tcp 22 20023

В файле с правилами для ASA:
- не должно быть пустых строк между правилами
- перед строками "object network" не должны быть пробелы
- перед остальными строками должен быть один пробел

Во всех правилах для ASA интерфейсы будут одинаковыми (inside,outside).
"""
import re 
from pprint import pprint
def convert_ios_nat_to_asa(cisco_nat_file_name_in, asa_nat_file_name_out):
    re_string = r"ip nat inside source static tcp (\S+) (\d+) interface \S+ (\d+)"
    re_comp = re.compile(re_string)
    res = list()
    with open("/home/vasily/pyneng/exercises/15_module_re/"+cisco_nat_file_name_in, "r") as f:
        for m in re.finditer(re_comp, f.read() ):
            res.append (m.groups())
            
        
    template = "object network LOCAL_{0}\n host {0}\n nat (inside,outside) static interface service tcp {1} {2}\n"
    #print(res)
    with open(asa_nat_file_name_out, "w") as f:
        for m in res:
            ip, port1, port2 = m;
            f.write(template.format(str(ip), str(port1), str(port2) ))

    
convert_ios_nat_to_asa("cisco_nat_config.txt","asa_nat_config.txt")