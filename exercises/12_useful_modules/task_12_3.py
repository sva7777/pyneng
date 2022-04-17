# -*- coding: utf-8 -*-
"""
Задание 12.3

Создать функцию print_ip_table, которая отображает таблицу доступных
и недоступных IP-адресов.

Функция ожидает как аргументы два списка:
* список доступных IP-адресов
* список недоступных IP-адресов

Результат работы функции - вывод на стандартный поток вывода таблицы вида:

Reachable    Unreachable
-----------  -------------
10.1.1.1     10.1.1.7
10.1.1.2     10.1.1.8
             10.1.1.9

"""
from tabulate import tabulate

reach= ["10.1.1.1", "10.1.1.2"]
un_reach = ["10.1.1.7", "10.1.1.8", "10.1.1.9"]

def print_ip_table(reachable, unreachable):
    table = {"Reachable": reachable, "Unreachable": unreachable}
    
    print ( tabulate(table, headers="keys")  )


print_ip_table(reach, un_reach)
