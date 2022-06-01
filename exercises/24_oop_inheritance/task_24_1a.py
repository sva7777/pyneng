# -*- coding: utf-8 -*-

"""
Задание 24.1a

Скопировать и дополнить класс CiscoSSH из задания 24.1.

Перед подключением по SSH необходимо проверить если ли в словаре с параметрами
подключения такие параметры: username, password, secret.
Если какого-то параметра нет, запросить значение у пользователя, а затем выполнять
подключение. Если все параметры есть, выполнить подключение.

In [1]: from task_24_1a import CiscoSSH

In [2]: device_params = {
   ...:         'device_type': 'cisco_ios',
   ...:         'host': '192.168.100.1',
   ...: }

In [3]: r1 = CiscoSSH(**device_params)
Введите имя пользователя: cisco
Введите пароль: cisco
Введите пароль для режима enable: cisco

In [4]: r1.send_show_command('sh ip int br')
Out[4]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

from base_connect_class import BaseSSH
from pprint import pprint

device_params = {"device_type": "cisco_ios", "host": "10.210.255.2"}

class CiscoSSH(BaseSSH):
    def ask_data(prompt):
        test= input("Введите {}:".format(prompt))
        return test
        
    def __init__(self, **device_params):
        if "username" not in device_params:
            device_params["username"]= CiscoSSH.ask_data("username")
        
        if "password" not in device_params:
            device_params["password"]= CiscoSSH.ask_data("password")
        
        if "secret" not in device_params:
            device_params["secret"]= CiscoSSH.ask_data("secret")
            
        super().__init__(**device_params)
        self.ssh.enable()

if __name__ == '__main__':
    r1= CiscoSSH(**device_params)
    pprint( r1.send_show_command('sh ip int br')  )