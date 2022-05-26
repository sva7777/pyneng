# -*- coding: utf-8 -*-
"""
Задание 20.5a

Создать функцию configure_vpn, которая использует
шаблоны из задания 20.5 для настройки VPN на маршрутизаторах
на основе данных в словаре data.

Параметры функции:
* src_device_params - словарь с параметрами подключения к устройству 1
* dst_device_params - словарь с параметрами подключения к устройству 2
* src_template - имя файла с шаблоном, который создает конфигурацию для строны 1
* dst_template - имя файла с шаблоном, который создает конфигурацию для строны 2
* vpn_data_dict - словарь со значениями, которые надо подставить в шаблоны

Функция должна настроить VPN на основе шаблонов
и данных на каждом устройстве с помощью netmiko.
Функция возвращает кортеж с выводом команд с двух
маршрутизаторов (вывод, которые возвращает метод netmiko send_config_set).
Первый элемент кортежа - вывод с первого устройства (строка),
второй элемент кортежа - вывод со второго устройства.

При этом, в словаре data не указан номер интерфейса Tunnel,
который надо использовать.
Номер надо определить самостоятельно на основе информации с оборудования.
Если на маршрутизаторе нет интерфейсов Tunnel,
взять номер 0, если есть взять ближайший свободный номер,
но одинаковый для двух маршрутизаторов.

Например, если на маршрутизаторе src такие интерфейсы: Tunnel1, Tunnel4.
А на маршрутизаторе dest такие: Tunnel2, Tunnel3, Tunnel8.
Первый свободный номер одинаковый для двух маршрутизаторов будет 5.
И надо будет настроить интерфейс Tunnel 5.

Для этого задания тест проверяет работу функции на первых двух устройствах
из файла devices.yaml. И проверяет, что в выводе есть команды настройки
интерфейсов, но при этом не проверяет настроенные номера тунелей и другие команды.
Они должны быть, но тест упрощен, чтобы было больше свободы выполнения.
"""
import re
import yaml
import netmiko
from task_20_5 import create_vpn_config
from pprint import pprint

data = {
    "tun_num": None,
    "wan_ip_1": "192.168.100.1",
    "wan_ip_2": "192.168.100.2",
    "tun_ip_1": "10.0.1.1 255.255.255.252",
    "tun_ip_2": "10.0.1.2 255.255.255.252",
}

def get_free_tunnel_number (src, dst):
    nums = [int(num) for num in re.findall(r"Tunnel(\d+)", src + dst)]
    if not nums:
        return 0
    diff = set(range(min(nums), max(nums) + 1)) - set(nums)
    if diff:
        return min(diff)
    else:
        return max(nums) + 1
    

def configure_vpn(src_device_params , dst_device_params, src_template, dst_template, vpn_data_dict):
    pprint(src_device_params)
    with netmiko.ConnectHandler(**src_device_params) as ssh1, netmiko.ConnectHandler(**dst_device_params) as ssh2:
        ssh1.enable()
        ssh2.enable()
        src_tunnels_output = ssh1.send_command("sh run | include ^interface Tunnel")
        dst_tunnels_output = ssh2.send_command("sh run | include ^interface Tunnel")
        tun_num = get_free_tunnel_number(src_tunnels_output, dst_tunnels_output)
        vpn_data_dict["tun_num"] = tun_num
        
        vpn1, vpn2 = create_vpn_config(src_template, dst_template, vpn_data_dict)
        
        temp1 = vpn1.split("\n")
        temp2 = vpn2.split("\n")
        
        temp1 = list (filter( lambda x: len(x)>0 , temp1))
        temp2 = list (filter( lambda x: len(x)>0 , temp2))

        
        pprint(temp1)
        pprint(temp2)
        
        output1 = ssh1.send_config_set(temp1) 
        output2 = ssh2.send_config_set(temp2)
        
    return output1, output2
if __name__ == "__main__":
    
    template1_file = "templates/gre_ipsec_vpn_1.txt"
    template2_file = "templates/gre_ipsec_vpn_2.txt"
    
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)
    
    pprint(configure_vpn(devices[0], devices[1], template1_file, template2_file, data) )