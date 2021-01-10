# data acqusition module 

import csv
from os import name
#import pandas as pd 
from init import *
import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file=db_name):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def init_db(database):
    # database = r"data\pythonsqlite2.db"    
    tables = [
    """ CREATE TABLE IF NOT EXISTS `data` (
	`name`	TEXT NOT NULL,
	`timestamp`	TEXT NOT NULL,
	`value`	TEXT NOT NULL,
	FOREIGN KEY(`value`) REFERENCES `iot_devices`(`name`)
    );""",
    """CREATE TABLE IF NOT EXISTS `iot_devices` (
	`sys_id`	INTEGER PRIMARY KEY,
	`name`	TEXT NOT NULL UNIQUE,
	`status`	TEXT,
    `units`	TEXT,
	`last_updated`	TEXT NOT NULL,
	`update_interval`	INTEGER NOT NULL,
	`address`	TEXT,
	`building`	TEXT,
	`room`	TEXT,
	`placed`	TEXT,
	`dev_type`	TEXT NOT NULL,
	`enabled`	INTEGER,    
	`state`	TEXT,
	`mode`	TEXT,
	`fan`	TEXT,
	`temperature`	REAL,
	`dev_pub_topic`	TEXT NOT NULL,
    `dev_sub_topic`	TEXT NOT NULL,
    `special`	TEXT		
    ); """    
    ]
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create tables
        for table in tables:
            create_table(conn, table)
        conn.close()            
    else:
        print("Error! cannot create the database connection.")


def csv_acq_data():
        conn= create_connection(db_name)
        
        try:
            if db_init:                
                data = pd.read_csv("data/homedata.csv")
                data.to_sql(table_name, conn, if_exists='append', index=False)                       
            else:
                data = pd.read_sql_query("SELECT * FROM "+table_name, conn)
        except Error as e:
            print(e)
        finally:    
            if conn:
                conn.close()    

def create_IOT_dev(name, status, units, last_updated, update_interval, address, building, room, placed, dev_type, enabled, state, mode, fan, temperature, dev_pub_topic, dev_sub_topic, special):
    """
    Create a new IOT device into the iot_devices table
    :param conn:
    :param :
    :return: sys_id
    """
    sql = ''' INSERT INTO iot_devices(name, status, units, last_updated, update_interval, address, building, room, placed, dev_type, enabled, state, mode, fan, temperature, dev_pub_topic, dev_sub_topic, special)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, status, units, last_updated, update_interval, address, building, room, placed, dev_type, enabled, state, mode, fan, temperature, dev_pub_topic, dev_sub_topic, special])
        conn.commit()
        re = cur.lastrowid
        conn.close()
        return re
    else:
        print("Error! cannot create the database connection.")    

def timestamp():
    return str(datetime.fromtimestamp(datetime.timestamp(datetime.now()))).split('.')[0]
    

def add_IOT_data(name, updated, value):
    """
    Add new IOT device data into the data table
    :param conn:
    :param :
    :return: last row id
    """
    sql = ''' INSERT INTO data(name, timestamp, value)
              VALUES(?,?,?) '''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, [name, updated, value])
        conn.commit()
        re = cur.lastrowid
        conn.close()
        return re
    else:
        print("Error! cannot create the database connection.")        

def read_IOT_data(table, name):
    """
    Query tasks by name
    :param conn: the Connection object
    :param name:
    :return: selected by name rows list
    """
    
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()        
        cur.execute("SELECT * FROM " + table +" WHERE name=?", (name,))
        rows = cur.fetchall()   
        return rows
    else:
        print("Error! cannot create the database connection.")   

def update_IOT_dev(tem_p):
    """
    update temperature of a IOT device by name
    :param conn:
    :param update:
    :return: project id
    """
    sql = ''' UPDATE iot_devices SET temperature = ? WHERE name = ?'''
    conn = create_connection()
    if conn is not None:
        cur = conn.cursor()
        cur.execute(sql, tem_p)
        conn.commit()
        conn.close()        
    else:
        print("Error! cannot create the database connection.") 

if __name__ == '__main__':
    if db_init:
        init_db(db_name)
    
    #numb =create_IOT_dev('DHT-1', 'on', 'celcius', timestamp(), 30, 'address', 'building', 'room', 'placed', 'dev_type', 'enabled', 'state', 'mode', 'fan', 'temperature', 'dev_pub_topic', 'dev_sub_topic', 'special')
    #numb =create_IOT_dev('DHT-2', 'on', 'celcius', timestamp(), 30, 'address', 'building', 'room', 'placed', 'dev_type', 'enabled', 'state', 'mode', 'fan', 'temperature', 'dev_pub_topic', 'dev_sub_topic', 'special')
    #numb =add_IOT_data('DTH-1', timestamp(), 27)
    #print(numb)

    #rows = read_IOT_data('data', 1)    
    #for row in rows:
    #print(rows[-1][2])
    update_IOT_dev(('12','DHT-1'))




# if __name__ == "__main__":    
#     data = acq_data()
#     # Preview the first 5 lines of the loaded data 
#     print(data.head())
