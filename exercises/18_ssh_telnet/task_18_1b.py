# -*- coding: utf-8 -*-
"""
Задание 18.1b

Скопировать функцию send_show_command из задания 18.1a и переделать ее таким образом,
чтобы обрабатывалось не только исключение, которое генерируется при ошибке
аутентификации на устройстве, но и исключение, которое генерируется, когда IP-адрес
устройства недоступен.

При возникновении ошибки, на стандартный поток вывода должно выводиться
сообщение исключения.

Для проверки измените IP-адрес на устройстве или в файле devices.yaml.
"""

import yaml
import netmiko

def send_show_command(device, command):
    result = None
    try: 
        with netmiko.ConnectHandler(**device) as ssh:
                ssh.enable()
                result = ssh.send_command(command)
    except netmiko.exceptions.NetmikoAuthenticationException as exe:
        print(exe)
    except netmiko.exceptions.NetmikoTimeoutException as exe:
        print(exe)

    
    return result


if __name__ == "__main__":
    command = "sh ip int br"
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        print(send_show_command(dev, command))