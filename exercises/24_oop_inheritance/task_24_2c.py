# -*- coding: utf-8 -*-

"""
Задание 24.2c

Скопировать класс MyNetmiko из задания 24.2b.
Проверить, что метод send_command кроме команду, принимает еще и дополнительные
аргументы, например, strip_command.

Если возникает ошибка, переделать метод таким образом, чтобы он принимал
любые аргументы, которые поддерживает netmiko.


In [2]: from task_24_2c import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [4]: r1.send_command('sh ip int br', strip_command=False)
Out[4]: 'sh ip int br\nInterface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

In [5]: r1.send_command('sh ip int br', strip_command=True)
Out[5]: 'Interface                  IP-Address      OK? Method Status                Protocol\nEthernet0/0                192.168.100.1   YES NVRAM  up                    up      \nEthernet0/1                192.168.200.1   YES NVRAM  up                    up      \nEthernet0/2                190.16.200.1    YES NVRAM  up                    up      \nEthernet0/3                192.168.230.1   YES NVRAM  up                    up      \nEthernet0/3.100            10.100.0.1      YES NVRAM  up                    up      \nEthernet0/3.200            10.200.0.1      YES NVRAM  up                    up      \nEthernet0/3.300            10.30.0.1       YES NVRAM  up                    up      '

"""

import re
from netmiko.cisco.cisco_ios import CiscoIosSSH

class ErrorInCommand(Exception):
    """
    Исключение генерируется, если при выполнении команды на оборудовании,
    возникла ошибка.
    """


device_params = {
    "device_type": "cisco_ios",
    "ip": "10.210.255.2",
    "username": "cisco",
    "password": "cisco",
    "secret": "cisco",
}

class MyNetmiko(CiscoIosSSH):
    def _check_error_in_command(self, command, output):
        regex = "% (?P<err>.+)"
        
        message = (
            'При выполнении команды "{cmd}" на устройстве {device} '
            'возникла ошибка "{error}"'
        )
            
        error_in_cmd = re.search(regex, output)
        
        if error_in_cmd:
            raise ErrorInCommand(message.format(cmd= command, device=self.host, error= error_in_cmd.group("err")  ))
        
        
        
    def __init__(self, **device_params):
        super().__init__(**device_params)
        print(self.host)
        self.enable()
    def send_command(self, command, **kwargs):
        output = super().send_command(command, **kwargs)
        self._check_error_in_command(command,output)
        return output
    def send_config_set(self, commands):
        result = ""
        
        if type (commands) == str:
            commands = [commands]
            
        for command in commands:
            output = super().send_config_set(commands)
            self._check_error_in_command(command, output)
            result = result + output
        return result


if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    print ( r1.send_command('sh ip int br', strip_command=False ) )
    