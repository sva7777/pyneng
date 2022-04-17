# -*- coding: utf-8 -*-
"""
Задание 12.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.

Функция ожидает как аргумент список IP-адресов.

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для проверки доступности IP-адреса, используйте команду ping (запуск ping через subprocess).
IP-адрес считается доступным, если выполнение команды ping отработало с кодом 0 (returncode).
Нюансы: на Windows returncode может быть равен 0 не только, когда ping был успешен,
но для задания нужно проверять именно код. Это сделано для упрощения тестов.

Ограничение: Все задания надо выполнять используя только пройденные темы.
"""
import subprocess

ip_test= ["8.8.8.8", "127.0.0.1", "8.8.4.4", "192.168.1.100"]

def ping_ip_addresses(ip_list):
    success_list = list()
    fail_list = list()
 
    for ip in ip_list:
        res = subprocess.run( ["ping", "-c 2", ip] )
        if res.returncode == 0 :
            success_list.append(ip)
        else:
            fail_list.append(ip)
    return success_list, fail_list
    
success, fail = ping_ip_addresses(ip_test)
print("t1 ")
print("success: "+ " ".join( success ) )
print("fail: " + " ".join( fail) )
