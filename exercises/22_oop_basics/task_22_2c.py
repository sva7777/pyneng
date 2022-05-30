# -*- coding: utf-8 -*-

"""
Задание 22.2c

Скопировать класс CiscoTelnet из задания 22.2b и изменить метод send_config_commands
добавив проверку команд на ошибки.

У метода send_config_commands должен быть дополнительный параметр strict:
* strict=True значит, что при обнаружении ошибки, необходимо сгенерировать
  исключение ValueError (значение по умолчанию)
* strict=False значит, что при обнаружении ошибки, надо только вывести
  на стандартный поток вывода сообщене об ошибке

Метод дожен возвращать вывод аналогичный методу send_config_set
у netmiko (пример вывода ниже). Текст исключения и ошибки в примере ниже.

Пример создания экземпляра класса:
In [1]: from task_22_2c import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

In [4]: commands_with_errors = ['logging 0255.255.1', 'logging', 'a']
In [5]: correct_commands = ['logging buffered 20010', 'ip http server']
In [6]: commands = commands_with_errors+correct_commands

Использование метода send_config_commands:

In [7]: print(r1.send_config_commands(commands, strict=False))
При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.
При выполнении команды "logging" на устройстве 192.168.100.1 возникла ошибка -> Incomplete command.
При выполнении команды "a" на устройстве 192.168.100.1 возникла ошибка -> Ambiguous command:  "a"
conf t
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#logging 0255.255.1
                   ^
% Invalid input detected at '^' marker.

R1(config)#logging
% Incomplete command.

R1(config)#a
% Ambiguous command:  "a"
R1(config)#logging buffered 20010
R1(config)#ip http server
R1(config)#end
R1#

In [8]: print(r1.send_config_commands(commands, strict=True))
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
<ipython-input-8-0abc1ed8602e> in <module>
----> 1 print(r1.send_config_commands(commands, strict=True))

...

ValueError: При выполнении команды "logging 0255.255.1" на устройстве 192.168.100.1 возникла ошибка -> Invalid input detected at '^' marker.

"""

import telnetlib
import re
from pprint import pprint
from textfsm import clitable

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
        self.ip = ip
        self.telnetSession =  telnetlib.Telnet(ip)
        self.telnetSession.read_until(b"Username")
        self._write_line(username)
        self.telnetSession.read_until(b"Password")
        self._write_line(password)
        self.telnetSession.read_until(b">")
        self._write_line("enable")
        self.telnetSession.read_until(b"Password")
        self._write_line(secret)
        self.telnetSession.read_until(b"#")
        self._write_line("terminal lengt 0")
        self.telnetSession.read_until(b"#")
        
        
        
        
    def _write_line(self, line):
        self.telnetSession.write(line.encode("ascii") + b"\n")

    def send_show_command(self, command, parse , templates="templates", index = "index" ):
        self._write_line(command)
        output = self.telnetSession.read_until(b"#").decode("utf-8")
        if parse:
            attributes = {"Command": command, "Vendor": "cisco_ios"}
            cli_table = clitable.CliTable(index, templates)
            cli_table.ParseCmd(output, attributes)
            return [dict(zip(cli_table.header, row)) for row in cli_table ]
            
        else:
            return output
    def _enter_config_mode(self):
        self._write_line("conf t")
        return self.telnetSession.read_until(b"(config)#").decode("utf-8")
        
    def _exit_config_mode(self):
        self._write_line("end")
        return self.telnetSession.read_until(b"#").decode("utf-8")
        
    def _send_config_command(self, command, strict):
        self._write_line(command)
        output = self.telnetSession.read_until(b"#").decode("utf-8")
        return output

    def _error_in_command(self, command, result, strict):
        regex = "% (?P<err>.+)"
        template = (
            'При выполнении команды "{cmd}" на устройстве {device} '
            "возникла ошибка -> {error}"
        )
        error_in_cmd = re.search(regex, result)
        if error_in_cmd:
            message = template.format(
                cmd=command, device=self.ip, error=error_in_cmd.group("err")
            )
            if strict:
                raise ValueError(message)
            else:
                print(message)
        
    def send_config_commands(self, commands, strict = True):
        result = self._enter_config_mode()
        
        if (type (commands) == str ):
            commands = [commands]
        
        for command in commands:
            result = result + self._send_config_command(command, strict=strict)
            self._error_in_command(command, result, strict=strict)
        
        result = result + self._exit_config_mode()
        
        return result
r1_params = {
            'ip': '10.210.255.2',
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco'
            }
   
r1 = CiscoTelnet(**r1_params)
pprint (r1.send_config_commands('logging 10.1.1.1', True) )