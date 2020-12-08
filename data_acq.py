# data acqusition module 

import csv
#import pandas as pd 
from init import *
import sqlite3
from sqlite3 import Error



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
 
def acq_data():
    if onboard:
        if is_glink:
            data = DOF()
        else:
            data = gLink200()
    else:
        conn= create_connection(db_name)
        table_name = 'K544_Data'
        try:
            if db_init:                
                data = pd.read_csv("data/data_home.csv")
                data.to_sql(table_name, conn, if_exists='append', index=False)                       
            else:
                data = pd.read_sql_query("SELECT * FROM "+table_name, conn)
        except Error as e:
            print(e)
        finally:    
            if conn:
                conn.close()    
    return data 


if __name__ == "__main__":    
    data = acq_data()
    # Preview the first 5 lines of the loaded data 
    print(data.head())
