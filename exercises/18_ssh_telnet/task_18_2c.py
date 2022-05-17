# -*- coding: utf-8 -*-
"""
Задание 18.2c

Скопировать функцию send_config_commands из задания 18.2b и переделать ее таким образом:

Если при выполнении команды возникла ошибка, спросить пользователя надо ли выполнять
остальные команды.

Варианты ответа [y]/n:
* y - выполнять остальные команды. Это значение по умолчанию,
  поэтому нажатие любой комбинации воспринимается как y
* n или no - не выполнять остальные команды

Функция send_config_commands по-прежнему должна возвращать кортеж из двух словарей:
* первый словарь с выводом команд, которые выполнились без ошибки
* второй словарь с выводом команд, которые выполнились с ошибками

Оба словаря в формате
* ключ - команда
* значение - вывод с выполнением команд

Проверить работу функции можно на одном устройстве.

Пример работы функции:

In [11]: result = send_config_commands(r1, commands)
Подключаюсь к 192.168.100.1...
Команда "logging 0255.255.1" выполнилась с ошибкой "Invalid input detected at '^' marker." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: y
Команда "logging" выполнилась с ошибкой "Incomplete command." на устройстве 192.168.100.1
Продолжать выполнять команды? [y]/n: n

In [12]: pprint(result)
({},
 {'logging': 'config term\n'
             'Enter configuration commands, one per line.  End with CNTL/Z.\n'
             'R1(config)#logging\n'
             '% Incomplete command.\n'
             '\n'
             'R1(config)#',
  'logging 0255.255.1': 'config term\n'
                        'Enter configuration commands, one per line.  End with '
                        'CNTL/Z.\n'
                        'R1(config)#logging 0255.255.1\n'
                        '                   ^\n'
                        "% Invalid input detected at '^' marker.\n"
                        '\n'
                        'R1(config)#'})

"""

import yaml
import netmiko
import re
from pprint import pprint


# списки команд с ошибками и без:
commands_with_errors = ["logging 0255.255.1", "logging", "a"]
correct_commands = ["logging buffered 20010", "ip http server"]

commands = commands_with_errors + correct_commands

class VasilyError(Exception):
    pass

def is_no_error_parse_result(command, result, device):
    r_string = r"% (?P<errmsg>.+)"
    error_string = 'Команда "{}" выполнилась с ошибкой "{}" на устройстве {}'
 
    match = re.search (r_string, result)
    
    if match:
        print (error_string.format(command, match.group("errmsg"), device) ) 
        
        print ("Продолжать выполнять команды? [y]/n:")
        inp= input()
        if inp == "n":
            raise VasilyError
        return False
    
    
    return True
    

def send_config_commands(device, config_commands, log = True):
    ok_dict = dict()
    error_dict = dict()
    if log:
        print(f"Подключаюсь к {device['host']}...")
    try: 
        with netmiko.ConnectHandler(**device) as ssh:
                ssh.enable()
                for command in config_commands:
                    
                    result = ssh.send_config_set(command)
                    
                    try:
                        res = is_no_error_parse_result(command, result, device["host"])
                    except VasilyError:
                        error_dict[command]= result
                        return (ok_dict, error_dict)
                                            
                    if res:
                        ok_dict[command]= result
                    else:
                        error_dict[command]= result
                
    except netmiko.exceptions.NetmikoAuthenticationException as exe:
        print(exe)
    except netmiko.exceptions.NetmikoTimeoutException as exe:
        print(exe)
    
    return (ok_dict, error_dict)


if __name__ == "__main__":
    with open("devices.yaml") as f:
        devices = yaml.safe_load(f)

    for dev in devices:
        pprint(send_config_commands(dev, commands, True))