# -*- coding: utf-8 -*-
"""
Задание 5.2a

Всё, как в задании 5.2, но, если пользователь ввел адрес хоста, а не адрес сети,
надо преобразовать адрес хоста в адрес сети и вывести адрес сети и маску,
как в задании 5.2.

Пример адреса сети (все биты хостовой части равны нулю):
* 10.0.1.0/24
* 190.1.0.0/16

Пример адреса хоста:
* 10.0.1.1/24 - хост из сети 10.0.1.0/24
* 10.0.5.195/28 - хост из сети 10.0.5.192/28

Если пользователь ввел адрес 10.0.1.1/24, вывод должен быть таким:

Network:
10        0         1         0
00001010  00000000  00000001  00000000

Mask:
/24
255       255       255       0
11111111  11111111  11111111  00000000


Проверить работу скрипта на разных комбинациях хост/маска, например:
    10.0.5.195/28, 10.0.1.1/24

Вывод сети и маски должен быть упорядочен также, как в примере:
- столбцами
- ширина столбца 10 символов (в двоичном формате
  надо добавить два пробела между столбцами
  для разделения октетов между собой)


Подсказка:
Есть адрес хоста в двоичном формате и маска сети 28. Адрес сети это первые 28 бит
адреса хоста + 4 ноля.
То есть, например, адрес хоста 10.1.1.195/28 в двоичном формате будет
bin_ip = "00001010000000010000000111000011"

А адрес сети будет первых 28 символов из bin_ip + 0000 (4 потому что всего
в адресе может быть 32 бита, а 32 - 28 = 4)
00001010000000010000000111000000

Ограничение: Все задания надо выполнять используя только пройденные темы.

"""
address = input("введите IPv4-сеть в формате 10.1.1.0/24 :")
ip_address, net_mask = address.split("/")
ip = ip_address.split(".")
ip_bin = "{:08b}{:08b}{:08b}{:08b}".format(int(ip[0]),int(ip[1]),int(ip[2]),int(ip[3]))
mask_bin = "1"*int(net_mask)+"0"*(32-int(net_mask))

network_ip = int(ip_bin,2)& int (mask_bin,2)
network_ip = "{:032b}".format(network_ip)

bulk = '''
Network:
{:10}{:10}{:10}{:10}
{:10}{:10}{:10}{:10}'''

ip_a = network_ip[0:8]
ip_b = network_ip[8:16]
ip_c = network_ip[16:24]
ip_d = network_ip[24:32]
print(bulk.format( str(int(ip_a,2)), str(int(ip_b,2)), str(int(ip_c,2)), str(int(ip_d,2)), ip_a, ip_b, ip_c, ip_d ) )

bulk_mask = '''
Mask:
/{}
{:10}{:10}{:10}{:10}
{:10}{:10}{:10}{:10}'''

bin_mask_a = mask_bin[0:8]
bin_mask_b = mask_bin[8:16]
bin_mask_c = mask_bin[16:24]
bin_mask_d = mask_bin[24:32]
print(bulk_mask.format(net_mask, str(int(bin_mask_a,2)), str(int(bin_mask_b,2)), str(int(bin_mask_c,2)), str(int(bin_mask_d,2)), bin_mask_a, bin_mask_b, bin_mask_c, bin_mask_d ) )












