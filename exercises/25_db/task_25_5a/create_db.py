import sqlite3
from os.path import exists

def create_db(filename, path_to_script):
    if exists(filename):
        print("База данных существует")
    else:
        print("Создаю базу данных...")
        

    with sqlite3.connect(filename) as conn:
        res =conn.execute("select count(*) from sqlite_master where type='table'")
        line = res.fetchone()
        number_of_tables = int(line[0])
        if number_of_tables ==0:
            with open(path_to_script,"r") as sql_file:
                    sql_script= sql_file.read()
            conn.executescript(sql_script)
            conn.commit()
    
    


db_file_name = "/home/vasily/pyneng/exercises/25_db/task_25_5a/task_25_5a.db"
path_to_script = "/home/vasily/pyneng/exercises/25_db/task_25_5a/dhcp_snooping_schema.sql"

if __name__ == '__main__':
    create_db(db_file_name, path_to_script)
    