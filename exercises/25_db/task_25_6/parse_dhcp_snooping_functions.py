import sqlite3
import yaml
import textfsm
from tabulate import tabulate
from pathlib import Path
from datetime import datetime, timedelta


def create_db(name, schema):
    
    with sqlite3.connect(name) as conn:
        res =conn.execute("select count(*) from sqlite_master where type='table'")
        line = res.fetchone()
        number_of_tables = int(line[0])
        if number_of_tables == 0:
            with open(schema,"r") as sql_file:
                    sql_script= sql_file.read()
            conn.executescript(sql_script)
            conn.commit()

def add_data_switches(db_file, filename):
    # filename is a list
    with sqlite3.connect(db_file) as conn:
        for yaml_file in filename:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                
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

def parse_file(file_name, template = "sh_ip_dhcp_snooping.template"):
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


def del_old_dhcp_record(conn, days_ago = 7):
    
    now = datetime.today().replace(microsecond=0)
    week_ago = now - timedelta(days_ago)
    
    delete_sql = "delete from dhcp where last_active <= ?"
    conn.execute(delete_sql, (str(week_ago), ))
    conn.commit()



def add_data(db_file, filename):
    # filename is a list
    with sqlite3.connect(db_file) as conn:
        for file in filename:
            file_name = Path(file).name
            switch_name = file_name.split("_")[0]
            result = parse_file(file)
            insert_records_into_dhcp(conn, switch_name, result)
    del_old_dhcp_record(conn, 7)    



def show_table_data(conn, table_name, column_name = None, value = None):
    # отобразить правильный заголовок
    if column_name is None:
        print("В таблице {} такие записи:".format(table_name) )
    else:
        print("Информация об устройствах с такими параметрами: {} {}".format(column_name, value) )
    
    print("Активные записи:")
    show_table_data_helper(conn, table_name, 1, column_name, value)
    print("Неактивные записи:")
    show_table_data_helper(conn, table_name, 0, column_name, value)    

def show_table_data_helper(conn, table_name, active , column_name =None , value =None):
    
    
    sql_query = "SELECT * from dhcp where active = ?"
    if column_name != None :
        sql_query = sql_query +" and " + column_name +" = ?"
        res = conn.execute(sql_query, (active, value) )
    else:
        res = conn.execute(sql_query, (active,))
        
    print(tabulate(res))

def get_data(db_file, key= None, value = None):
    with sqlite3.connect(db_file) as conn:
        show_table_data(conn, "dhcp", key, value)

def get_all_data(db_file):
    get_data(db_file)