# -*- coding: utf-8 -*-

"""
Задание 23.1a

Скопировать и изменить класс IPAddress из задания 23.1.

Добавить два строковых представления для экземпляров класса IPAddress.
Как дожны выглядеть строковые представления, надо определить из вывода ниже:

Создание экземпляра
In [5]: ip1 = IPAddress('10.1.1.1/24')

In [6]: str(ip1)
Out[6]: 'IP address 10.1.1.1/24'

In [7]: print(ip1)
IP address 10.1.1.1/24

In [8]: ip1
Out[8]: IPAddress('10.1.1.1/24')

In [9]: ip_list = []

In [10]: ip_list.append(ip1)

In [11]: ip_list
Out[11]: [IPAddress('10.1.1.1/24')]

In [12]: print(ip_list)
[IPAddress('10.1.1.1/24')]

"""
class IPAddress:
    def __init__(self, ip_mask):
        
        # check general format
        if ip_mask.count("/") != 1:
            raise ValueError
                    
        ip, mask = ip_mask.split("/")
        
        # check mask
        if not mask.isdigit():
            raise ValueError
        
        if int(mask)<8 or int(mask) >24:
            raise ValueError
        
        # check ip
        if ip.count(".") != 3:
            raise ValueError
                
        ip_array = ip.split(".")
        
        for ip_item in ip_array:
            if not ip_item.isdigit():
                raise ValueError
            if int(ip_item) <0 or int(ip_item) >240:
                raise ValueError
        
        self.ip = ip
        self.mask = int(mask)
        
    def __str__(self):
        return "IP address " +self.ip +"/"+str(self.mask)
        
    def __repr__(self):
        return "IPAddress('"+self.ip+"/"+str(self.mask)+"')"
    

ip= IPAddress("10.1.1.1/24")
print (str(ip))

ip_list = []
ip_list.append(ip)
print( ip_list) 