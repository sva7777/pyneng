# -*- coding: utf-8 -*-
"""
Задание 5.2

Запросить у пользователя ввод IP-сети в формате: 10.1.1.0/24

Затем вывести информацию о сети и маске в таком формате:

Network:
10        1         1         0
00001010  00000001  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000

Проверить работу скрипта на разных комбинациях сеть/маска.

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)

Подсказка: Получить маску в двоичном формате можно так:
In [1]: "1" * 28 + "0" * 4
Out[1]: '11111111111111111111111111110000'


Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
address = input("введите IPv4-сеть в формате 10.1.1.0/24 :")
separator = address.split("/")
ip_separator = separator[0].split(".")
bulk = '''
Network:
{:10}{:10}{:10}{:10}
{:10}{:10}{:10}{:10}'''
print(bulk.format( ip_separator[0],ip_separator[1], ip_separator[2], ip_separator[3], format(int(ip_separator[0]),"08b"), format(int(ip_separator[1]),"08b"), format(int(ip_separator[2]),"08b"), format(int(ip_separator[3]),"08b")   ) )
bulk_mask = '''
Mask:
/{}
{:10}{:10}{:10}{:10}
{:10}{:10}{:10}{:10}
'''
bin_mask = "1"*int(separator[1])+"0"*(32-int(separator[1]))
bin_mask_a = bin_mask[0:8]
bin_mask_b = bin_mask[8:16]
bin_mask_c = bin_mask[16:24]
bin_mask_d = bin_mask[24:32]
print(bulk_mask.format(separator[1], str(int(bin_mask_a,2)), str(int(bin_mask_b,2)), str(int(bin_mask_c,2)), str(int(bin_mask_d,2)), bin_mask_a, bin_mask_b, bin_mask_c, bin_mask_d ) )



