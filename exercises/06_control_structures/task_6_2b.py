# -*- coding: utf-8 -*-
"""
Задание 6.2b

Сделать копию скрипта задания 6.2a.

Дополнить скрипт: Если адрес был введен неправильно, запросить адрес снова.

Если адрес задан неправильно, выводить сообщение: 'Неправильный IP-адрес'
Сообщение "Неправильный IP-адрес" должно выводиться только один раз,
даже если несколько пунктов выше не выполнены.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
ip_string = input("введите IP адрес в формате 10.0.1.1 :")

if ip_string.count(".") == 3:
    ip_a,ip_b,ip_c,ip_d = ip_string.split(".")
    if  (not ip_a.isdigit() )   or (not ip_b.isdigit() ) or (not ip_c.isdigit() ) or (not ip_d.isdigit() ) :
        print("Неправильный IP-адрес")
    elif ( ( not int(ip_a) in range (0,256)) or (not int(ip_b) in range (0,256)) or (not int(ip_c) in range (0,256))  or (not int(ip_d) in range (0,256))):
        print("Неправильный IP-адрес")
    elif ( int(ip_a) in range(1,224) ):
        print("unicast")
    elif (int(ip_a) in range (224,240)):
        print("multicast")
    elif ( int(ip_a)==255 and int(ip_b) == 255 and int (ip_c) == 255 and int(ip_d) ==255):
        print("local broadcast")
    elif ( int(ip_a) == 0 and int(ip_b) == 0 and int(ip_c) == 0 and int(ip_d) == 0):
        print("unassigned")
    else:
        print("unused")
else:
    print("Неправильный IP-адрес")