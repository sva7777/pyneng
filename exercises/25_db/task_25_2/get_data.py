import sys
import sqlite3

from pprint import pprint

def get_table_columns_name(conn, table_name):
    r = []
    sql_query = "PRAGMA table_info({})"
    res= conn.execute(sql_query.format(table_name) )
    for line in res:
        r.append( line[1] )
        
    return r
    
    

db_file_name= "/home/vasily/pyneng/exercises/25_db/task_25_1/task_25_1.db"

if __name__ == '__main__':
    arg_count = len(sys.argv)
    
    if arg_count != 1 and arg_count !=3:
        print("Пожалуйста, введите два или ноль аргументов")
    else:
        with sqlite3.connect(db_file_name) as conn:
            if arg_count ==3:
                columns = get_table_columns_name(conn, "dhcp")
                if argv[1] not in columns:
                    pprint("Данный параметр не поддерживается.")
                    #Допустимые значения параметров: mac, ip, vlan, interface, switch

            
        
        