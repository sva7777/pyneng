# -*- coding: utf-8 -*-
"""
Задание 4.6

Обработать строку ospf_route и вывести информацию на стандартный поток вывода в виде:
Prefix                10.0.24.0/24
AD/Metric             110/41
Next-Hop              10.0.13.3
Last update           3d18h
Outbound Interface    FastEthernet0/0

Ограничение: Все задания надо выполнять используя только пройденные темы.

Предупреждение: в разделе 4 тесты можно легко "обмануть" сделав нужный вывод,
без получения результатов из исходных данных с помощью Python.
Это не значит, что задание сделано правильно, просто на данном этапе сложно иначе
проверять результат.
"""

ospf_route = "      10.0.24.0/24 [110/41] via 10.0.13.3, 3d18h, FastEthernet0/0"
first_split = ospf_route.strip().split(", ")
second_split= first_split[0].split(" ")
print("{:21} {}".format("Prefix",second_split[0]) )
print("{:21} {}".format("AD/Metric",second_split[1].strip("[]")))
print("{:21} {}".format("Next-Hop",second_split[3]))
print("{:21} {}".format("Last update",first_split[1]))
print("{:21} {}".format ("Outbound Interface",first_split[2]))
