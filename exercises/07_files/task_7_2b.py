# -*- coding: utf-8 -*-
"""
Задание 7.2b

Переделать скрипт из задания 7.2a: вместо вывода на стандартный поток вывода,
скрипт должен записать полученные строки в файл

Имена файлов нужно передавать как аргументы скрипту:
 * имя исходного файла конфигурации
 * имя итогового файла конфигурации

При этом, должны быть отфильтрованы строки, которые содержатся в списке ignore
и строки, которые начинаются на '!'.

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""

ignore = ["duplex", "alias", "configuration"]
from sys import argv

file_name = argv[1]
out_file = argv[2]

with open(file_name, "r") as input_f , open(out_file,"w") as output_f :
    for line in input_f :
        words= line.split()
        
        if (not line.startswith("!")  ) and (not  set(words) & set(ignore) )  :
            output_f.write(line)            