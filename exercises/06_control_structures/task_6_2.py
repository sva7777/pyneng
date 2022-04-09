# -*- coding: utf-8 -*-
"""
Задание 6.2

Запросить у пользователя ввод IP-адреса в формате 10.0.1.1
В зависимости от типа адреса (описаны ниже), вывести на стандартный поток вывода:
   'unicast' - если первый байт в диапазоне 1-223
   'multicast' - если первый байт в диапазоне 224-239
   'local broadcast' - если IP-адрес равен 255.255.255.255
   'unassigned' - если IP-адрес равен 0.0.0.0
   'unused' - во всех остальных случаях

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""

ip_string = input("введите IP адрес в формате 10.0.1.1 :")
ip_a,ip_b,ip_c,ip_d = ip_string.split(".")

if ( int(ip_a) in range(1,224) ):
    print("unicast")
elif (int(ip_a) in range (224,240)):
    print("multicast")
elif ( int(ip_a)==255 and int(ip_b) == 255 and int (ip_c) == 255 and int(ip_d) ==255):
    print("local broadcast")
elif ( int(ip_a) == 0 and int(ip_b) == 0 and int(ip_c) == 0 and int(ip_d) == 0):
    print("unassigned")
else:
    print("unused")
