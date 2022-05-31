# -*- coding: utf-8 -*-

"""
Задание 23.3a

В этом задании надо сделать так, чтобы экземпляры класса Topology
были итерируемыми объектами.
Основу класса Topology можно взять из любого задания 22.1x или задания 23.3.

После создания экземпляра класса, экземпляр должен работать как итерируемый объект.
На каждой итерации должен возвращаться кортеж, который описывает одно соединение.
Порядок вывода соединений может быть любым.


Пример работы класса:

In [1]: top = Topology(topology_example)

In [2]: for link in top:
   ...:     print(link)
   ...:
(('R1', 'Eth0/0'), ('SW1', 'Eth0/1'))
(('R2', 'Eth0/0'), ('SW1', 'Eth0/2'))
(('R2', 'Eth0/1'), ('SW2', 'Eth0/11'))
(('R3', 'Eth0/0'), ('SW1', 'Eth0/3'))
(('R3', 'Eth0/1'), ('R4', 'Eth0/0'))
(('R3', 'Eth0/2'), ('R5', 'Eth0/0'))


Проверить работу класса.
"""
class Topology:
    def __init__(self, topology_dict):
        self.topology = self._normalize(topology_dict)
        
    def _normalize(self, topology_dict):
        res = dict()
        for dev_left, dev_rigth in topology_dict.items():
            if  dev_rigth in res.keys():
                continue
            else:
                res[dev_left]=dev_rigth
        return res

    def delete_link(self, left, right):
        if left in self.topology.keys() and self.topology[ left] == right:
            self.topology.pop(left)
        elif right in self.topology.keys() and self.topology[ right] == left:
                self.topology.pop(right)
        else:
            print("Такого соединения нет")
    def delete_node(self, node ):
        res = dict()
        flag = False
        for dev_left, dev_rigth in self.topology.items():
            l_l,r_d = dev_left 
            l_r,r_r = dev_rigth
            if l_l != node and l_r != node:
                res[dev_left] = dev_rigth
            else:
                flag = True
                
        if flag:
            self.topology = res
        else:
            print("Такого устройства нет")
    def add_link(self, left, right):
        if left in self.topology.keys() and self.topology[left] == right:
            print("Такое соединение существует")
        elif left in self.topology.keys() or right in self.topology.keys():
            print("Cоединение с одним из портов существует")
        else:
            self.topology[left] = right
    def __add__(self, other):
        temp = Topology( {**self.topology, ** other.topology } )
        return temp 
    
    def __iter__(self):
        
        return iter(self.topology.items())


topology_example = {
    ("R1", "Eth0/0"): ("SW1", "Eth0/1"),
    ("R2", "Eth0/0"): ("SW1", "Eth0/2"),
    ("R2", "Eth0/1"): ("SW2", "Eth0/11"),
    ("R3", "Eth0/0"): ("SW1", "Eth0/3"),
    ("R3", "Eth0/1"): ("R4", "Eth0/0"),
    ("R3", "Eth0/2"): ("R5", "Eth0/0"),
    ("SW1", "Eth0/1"): ("R1", "Eth0/0"),
    ("SW1", "Eth0/2"): ("R2", "Eth0/0"),
    ("SW1", "Eth0/3"): ("R3", "Eth0/0"),
}


t1 = Topology(topology_example)
for link in t1:
   print(link)
   