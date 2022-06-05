import sqlite3
import yaml
import glob
import textfsm
import sys

from os.path import exists
from create_db import db_file_name
from pprint import pprint
from pathlib import Path

def add_data_to_switch_table(conn, yaml_file):
    print("Добавляю данные в таблицу switches...")
    with open(yaml_file)as f:
        data= yaml.safe_load(f)
    
    switches= data['switches']
    
    # Строка для вставки
    sql_insert_switches = "INSERT INTO switches VALUES (?,?)"
    
    for switch, description in switches.items():
        try:
            conn.execute(sql_insert_switches,(switch, description) )
        except sqlite3.IntegrityError as ex:
            error_message= "При добавлении данных: {} Возникла ошибка: {}"
            print (error_message.format((switch, description), ex))
        conn.commit()   
        
    
def parse_file(file_name, template):
    with open(file_name, "r") as f:
        output = f.read()
    
    with open (template, "r") as f:
        fsm = textfsm.TextFSM(f)
        result = fsm.ParseText(output)
        
    return [dict(zip(fsm.header, row)) for row in result]
    

def insert_records_into_dhcp(conn, switch_name, records):
    
    # Устновить флаг active = False для всех записей данного switch
    
    sql_set_active_flag_false = "UPDATE dhcp SET active =0 WHERE switch = ?"
    conn.execute(sql_set_active_flag_false, (switch_name,))
    conn.commit()
    
    sql_replace_dhcp= "replace into dhcp values (?,?,?,?,?,?, datetime('now') )"
    
    
    
    for line in records:
        try:
            to_insert = (line['mac'],line['ip'], line['vlan'], line['intf'],switch_name, 1)  
            conn.execute(sql_replace_dhcp, to_insert )
            
        except sqlite3.IntegrityError as ex:
            error_message= "При добавлении данных: {} Возникла ошибка: {}"
            print (error_message.format(to_insert, ex))
        conn.commit()   

    
    

def add_data_to_dhcp_snooping(conn, dir_name, pattern, template):
    print("Добавляю данные в таблицу dhcp...")
    for name in glob.glob(dir_name+"/"+pattern):
        file = Path(name).name
        switch_name = file.split("_")[0]
        
        result = parse_file(name, template)
            
        insert_records_into_dhcp(conn, switch_name, result)
        
    

switches_yaml_file = "/home/vasily/pyneng/exercises/25_db/task_25_3/switches.yml"


file_pattern ="*_dhcp_snooping.txt"
fsm_template = "/home/vasily/pyneng/exercises/25_db/task_25_3/sh_ip_dhcp_snooping.template"

if __name__ == '__main__':
    arg_count = len(sys.argv) 
    
    if arg_count != 2:
        print("В качестве параметра укажите путь к файлам *_dhcp_snooping.txt")
        exit()
    
    dir_name = sys.argv[1]
    
    if not exists(db_file_name):
        print("База данных не существует. Перед добавлением данных, ее надо создать")
    else:
        with sqlite3.connect(db_file_name) as conn:
            add_data_to_switch_table(conn, switches_yaml_file)
            add_data_to_dhcp_snooping(conn, dir_name, file_pattern, fsm_template)
    