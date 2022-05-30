# -*- coding: utf-8 -*-

"""
Задание 22.2b

Скопировать класс CiscoTelnet из задания 22.2a и добавить метод send_config_commands.


Метод send_config_commands должен уметь отправлять одну команду конфигурационного
режима и список команд.
Метод должен возвращать вывод аналогичный методу send_config_set у netmiko
(пример вывода ниже).

Пример создания экземпляра класса:
In [1]: from task_22_2b import CiscoTelnet

In [2]: r1_params = {
   ...:     'ip': '192.168.100.1',
   ...:     'username': 'cisco',
   ...:     'password': 'cisco',
   ...:     'secret': 'cisco'}

In [3]: r1 = CiscoTelnet(**r1_params)

Использование метода send_config_commands:

In [5]: r1.send_config_commands('logging 10.1.1.1')
Out[5]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#logging 10.1.1.1\r\nR1(config)#end\r\nR1#'

In [6]: r1.send_config_commands(['interface loop55', 'ip address 5.5.5.5 255.255.255.255'])
Out[6]: 'conf t\r\nEnter configuration commands, one per line.  End with CNTL/Z.\r\nR1(config)#interface loop55\r\nR1(config-if)#ip address 5.5.5.5 255.255.255.255\r\nR1(config-if)#end\r\nR1#'

"""

import telnetlib
from pprint import pprint
from textfsm import clitable

class CiscoTelnet:
    def __init__(self, ip, username, password, secret):
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
    def enter_config_mode(self):
        self._write_line("conf t")
        return self.telnetSession.read_until(b"(config)#").decode("utf-8")
        
    def exit_config_mode(self):
        self._write_line("end")
        return self.telnetSession.read_until(b"#").decode("utf-8")
        
    def send_config_command(self, command):
        self._write_line(command)
        output = self.telnetSession.read_until(b"#").decode("utf-8")
        return output
        
    def send_config_commands(self, commands):
        result = self.enter_config_mode()
        
        if (type (commands) == str ):
            result = result + self.send_config_command(commands)
        else:
            for command in commands:
                result = result + self.send_config_command(command)
        
        result = result + self.exit_config_mode()
        
        return result
r1_params = {
            'ip': '10.210.255.2',
            'username': 'cisco',
            'password': 'cisco',
            'secret': 'cisco'
            }
   
r1 = CiscoTelnet(**r1_params)
pprint (r1.send_config_commands('logging 10.1.1.1') )



