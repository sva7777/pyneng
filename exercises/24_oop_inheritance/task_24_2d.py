# -*- coding: utf-8 -*-

"""
Задание 24.2d

Скопировать класс MyNetmiko из задания 24.2c или задания 24.2b.

Добавить параметр ignore_errors в метод send_config_set.
Если передано истинное значение, не надо выполнять проверку на ошибки и метод должен
работать точно так же как метод send_config_set в netmiko.
Если значение ложное, ошибки должны проверяться.

По умолчанию ошибки должны игнорироваться.


In [2]: from task_24_2d import MyNetmiko

In [3]: r1 = MyNetmiko(**device_params)

In [6]: r1.send_config_set('lo')
Out[6]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [7]: r1.send_config_set('lo', ignore_errors=True)
Out[7]: 'config term\nEnter configuration commands, one per line.  End with CNTL/Z.\nR1(config)#lo\n% Incomplete command.\n\nR1(config)#end\nR1#'

In [8]: r1.send_config_set('lo', ignore_errors=False)
---------------------------------------------------------------------------
ErrorInCommand                            Traceback (most recent call last)
<ipython-input-8-704f2e8d1886> in <module>()
----> 1 r1.send_config_set('lo', ignore_errors=False)

...
ErrorInCommand: При выполнении команды "lo" на устройстве 192.168.100.1 возникла ошибка "Incomplete command."
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
    def send_config_set(self, commands, **kwargs):
        result = ""
        
        if type (commands) == str:
            commands = [commands]
            
        for command in commands:
            output = super().send_config_set(commands)
            if 'ignore_errors' in kwargs.keys():
                if not kwargs['ignore_errors']:           
                    self._check_error_in_command(command, output)
                else:
                    result= result + output
        return result


if __name__ == '__main__':
    r1 = MyNetmiko(**device_params)
    print ( r1.send_config_set('sh ip int br', ignore_errors=False ) )
    