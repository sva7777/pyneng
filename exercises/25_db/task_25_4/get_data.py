import sys
import sqlite3
from tabulate import tabulate


def get_table_columns_name(conn, table_name):
    r = []
    sql_query = "PRAGMA table_info({})"
    res= conn.execute(sql_query.format(table_name) )
    for line in res:
        r.append( line[1] )
        
    return r

def show_table_data_helper(conn, table_name, active , column_name =None , value =None):
    
    
    sql_query = "SELECT * from dhcp where active = ?"
    if column_name != None :
        sql_query = sql_query +" and " + column_name +" = ?"
        res = conn.execute(sql_query, (active, value) )
    else:
        res = conn.execute(sql_query, (active,))
        
    print(tabulate(res))
    

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

db_file_name= "/home/vasily/pyneng/exercises/25_db/task_25_3/task_25_3.db"

if __name__ == '__main__':
    arg_count = len(sys.argv)
    
    if arg_count != 1 and arg_count !=3:
        print("Пожалуйста, введите два или ноль аргументов")
    else:
        with sqlite3.connect(db_file_name) as conn:
            if arg_count ==3:
                columns = get_table_columns_name(conn, "dhcp")
                if sys.argv[1] not in columns:
                    print("Данный параметр не поддерживается.")
                    # Отобразить поддерживаемые колонки
                    print("Допустимые значения параметров: {}".format(columns))
                else:
                    column_name = sys.argv[1]
                    value= sys.argv[2]
                    show_table_data(conn, "dhcp", column_name, value)
            else: 
                show_table_data(conn, "dhcp")
                