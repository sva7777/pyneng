# -*- coding: utf-8 -*-
"""
Задание 19.1

Создать функцию ping_ip_addresses, которая проверяет пингуются ли IP-адреса.
Проверка IP-адресов должна выполняться параллельно в разных потоках.

Параметры функции ping_ip_addresses:
* ip_list - список IP-адресов
* limit - максимальное количество параллельных потоков (по умолчанию 3)

Функция должна возвращать кортеж с двумя списками:
* список доступных IP-адресов
* список недоступных IP-адресов

Для выполнения задания можно создавать любые дополнительные функции.

Для проверки доступности IP-адреса, используйте ping.

Подсказка о работе с concurrent.futures:
Если необходимо пинговать несколько IP-адресов в разных потоках,
надо создать функцию, которая будет пинговать один IP-адрес,
а затем запустить эту функцию в разных потоках для разных
IP-адресов с помощью concurrent.futures (это надо сделать в функции ping_ip_addresses).
"""


import subprocess
import yaml
import logging
from pprint import pprint
from concurrent.futures import ThreadPoolExecutor


def ping_ip(ip_address):
    reply = subprocess.run(['ping', '-c', '3', '-n', ip_address],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                encoding='utf-8')
    if reply.returncode == 0:
        return True
    else:
        return False

def ping_ip_addresses(ip_list , limit =3):
    ok_ping = list()
    not_ping = list()
    
    with ThreadPoolExecutor(max_workers=limit) as executor:
        result = executor.map(ping_ip, ip_list)
        for ip, res  in zip(ip_list, result):
            if res:
                ok_ping.append(ip)
            else:
                not_ping.append(ip)
    
    return (ok_ping, not_ping)


if __name__ == "__main__":
    ip_s= list()
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        ip_s.append(dev["host"])
    
    pprint (ping_ip_addresses(ip_s) )